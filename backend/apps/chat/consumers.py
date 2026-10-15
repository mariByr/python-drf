import datetime
from typing import cast

from django.contrib.auth import get_user_model
from django.db.models.expressions import F
from django.db.models.query_utils import Q

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.chat.models import ChatRoomModel, MessageModel

UserModel = get_user_model()

class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.user_name = None

    async def connect(self):
        if not self.scope['user']:
            return await self.close()

        await self.accept()
        await self.send_json({
            'type': 'current_user',
            'userId': self.scope['user'].id
        })

        self.room_name =  cast(
            str,
            self.scope['url_route']['kwargs'].get('room')
        )

        self.room, _ = await ChatRoomModel.objects.aget_or_create(name=self.room_name)
        self.user_name = await self.get_profile_name()

        #make new groups to comun
        await self.channel_layer.group_add(
            f'user_{self.scope["user"].id}',#створення персональних груп
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        messages = await self.get_last_five_messages()

        for name, text in messages:
            await self.sender({
                'message': text,
                'user': name,
                'request_id': str(datetime.datetime.now())
            })

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': f'{self.user_name} connected to chat'
            }
        )
    async def sender(self, data):

        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        await MessageModel.objects.acreate(
            room=self.room,
            user=self.scope['user'],
            text=data['text'])
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message':data['text'],
                'user':f"{self.scope['user'].id}_{self.user_name}",
                'id':request_id
            }
        )

    @action()
    async def send_private_message(self, data, request_id, action):
        sender_id = self.scope['user'].id #створюємо передавача
        recipient_id = int(data['userId']) #створюємо отримувача приватного повідомлення

        user_ids = sorted([sender_id, recipient_id])
        private_room_name = f"private_{user_ids[0]}_{user_ids[1]}"

        private_room, is_created = await ChatRoomModel.objects.aget_or_create(
            name=private_room_name,
            is_private=True

        )

        recipient = await UserModel.objects.aget(pk=recipient_id)

        await private_room.users.aadd(#додаємо до приватної кімнати тотримувача іпередача
            recipient,
            self.scope['user']
        )

        await MessageModel.objects.acreate(#створюємо в бд запис про повідомлення
            room=private_room,
            user=self.scope['user'],
            text=data['text']
        )

        await self.channel_layer.group_send(#посилаємо повідомлення отримувачу
            f"user_{recipient_id}",
            {
                'type': 'sender',
                'message': data['text'],
                'user': f"{sender_id}_{self.user_name}",
                'room': private_room_name,
                'is_private': True,
                'id': request_id
            })
        if sender_id != recipient_id:
            await self.channel_layer.group_send(
                f"user_{sender_id}",
                {
                    'type': 'sender',
                    'message': data['text'],
                    'user': f"{sender_id}_{self.user_name}",
                    'sender_id': sender_id,
                    'room': private_room_name,
                    'is_private': True,
                    'id': request_id
                })
        
    @database_sync_to_async
    def get_profile_name(self):
        user = self.scope['user']

        return user.profile.name


    @database_sync_to_async
    def get_last_five_messages(self):

        res = MessageModel.objects.filter(
            Q(room=self.room)|(Q(room__is_private=True)&Q(room__users__in=[self.scope['user']]))
        ).annotate(
            name=F('user__profile__name'), pk=F('user__pk')
        ).values('text', 'name', 'pk').order_by('-id')[:5]
        print(res, '(((((((((((((((((((((((((((((((((((((((((((((')
        return reversed([(f'{message['pk']}_{message['name']}', message['text']) for message in res])