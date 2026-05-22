from rest_framework import serializers, status
from rest_framework.response import Response
from apps.pizza.models import PizzaModel

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaModel
        fields = ('id','name','size','price','created_at','updated_at')
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=100)
    # size = serializers.IntegerField()
    # price = serializers.FloatField()
    # created_at= serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)
    #
    # def create(self, validated_data):
    #     return PizzaModel.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     for k,v  in validated_data.items():
    #         setattr(instance, k, v)
    #     instance.save()
    #     return instance
    # def delete(self,*args, **kwargs):
    #     pk=kwargs['pk']
    #     try:
    #         PizzaModel.objects.get(pk=pk).delete()
    #     except PizzaModel.DoesNotExist:
    #         return Response(status.HTTP_204_NO_CONTENT)
    #     return Response(status.HTTP_204_NO_CONTENT)

