from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import status, request

# Create your views here.
#Створити сутність pizza (поля довільні 3-4 шт)
# та реалізувати над нею всі CRUD операції (Create, Read, Update, Delete)
from rest_framework.response import Response
from rest_framework.views import APIView
from pizza.models import PizzaModel
from pizza.serializers import PizzaSerializer

class PizzaListCreateView(APIView):
    def get(self,*args, **kwargs):
        pizzas = PizzaModel.objects.all()
        serializer=PizzaSerializer(pizzas,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, *args, **kwargs):
        serializer= PizzaSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class PizzaRetrieveUpdateDestroyView(APIView):
        def get(self, *args, **kwargs):
            pk=self.kwargs['pk']
            try:
                pizza= PizzaModel.objects.get(pk=pk)
            except PizzaModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer=PizzaSerializer(pizza)
            return Response(serializer.data,status=status.HTTP_200_OK)
            data=self.request.data
            serializer = PizzaSerializer(pizza, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        def put(self, *args, **kwargs):
            pk=kwargs['pk']
            try:
                pizza= PizzaModel.objects.get(pk=pk)
            except PizzaModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            data = self.request.data
            serializer = PizzaSerializer(pizza, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)


        def delete(self, *args, **kwargs):
            pk=kwargs['pk']
            try:
                pizza= PizzaModel.objects.get(pk=pk)
                pizza.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except PizzaModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)





