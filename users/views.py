from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms import model_to_dict

from users import serializer
from users.models import UserModel
from rest_framework import status

from users.serializer import UserSerializer


class UsersListCreateView(APIView):#один ендпоінт щоб витягнути всіх юзерів і додати нового

    def get (self,*args,**kwargs):
        users = UserModel.objects.all()
        serialiser = UserSerializer(instance=users,many=True)
        # response = [model_to_dict(user) for user in users]
        return Response(serialiser.data,status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = UserSerializer(data=data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = UserModel(
        #     name=data['name'],
        #     age=data['age'],
        #     status=data['status'],
        #     weight=data['weight'],
        # )
        # user.save() перший метод створення обєкту з внесених користувачем  даних і збереження в bd
        # 2 metod
        # user = UserModel.objects.create(**serializer.data)
        # response = model_to_dict(user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserRetriveUpdateDeleteView(APIView):
   def get(self, *args,**kwargs):
      pk = kwargs['pk']
      try:
        user = UserModel.objects.get(pk=pk)
      except UserModel.DoesNotExist:
         return Response(f'User{pk} not found')
      serializer = UserSerializer(user)
      return Response(serializer.data,status=status.HTTP_200_OK)

   def put(self, *args,**kwargs):
       pk = kwargs['pk']
       try:
           user = UserModel.objects.get(pk=pk)
       except UserModel.DoesNotExist:
           return Response(f'User{pk} not found')
       data = self.request.data
       serializer =  UserSerializer(instance=user,data=data)
       serializer.is_valid(raise_exception=True)
       serializer.save()

       return Response(serializer.data,status=status.HTTP_200_OK)

   def delete(self, *args,**kwargs):
       pk = kwargs['pk']
       try:
           user = UserModel.objects.get(pk=pk).delete()
       except UserModel.DoesNotExist:
           return Response(f'User{pk} not found')
       return Response(status=status.HTTP_204_NO_CONTENT)




