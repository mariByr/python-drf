
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from core.services.jwt_service import JWTService, SocketToken

#цей мідлвар замість бейсмідлвар

@database_sync_to_async
def get_user(token: str | None):
    try:
        return JWTService.verify_token(token, SocketToken)
    except (Exception,):
        pass
  #  авторизація користувача під час сокетпідключення
#декодуємо зі скопу бінарні дані щоб витягнути токен і за ним знайти користувача

class AuthSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = dict(
            [item.split('=') for item in scope['query_string'].decode('utf-8').split('&') if item]
        ).get('token', None)
        print('TOKEN:', token)

        scope['user'] = await get_user(token=token)

        print('USER:', scope['user'])
        return await super().__call__(scope, receive, send)