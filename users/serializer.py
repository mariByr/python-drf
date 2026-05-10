from rest_framework import serializers
from users.models import UserModel
#призначений дл явалідації даних і конвертувагння в джейсоноподібні обєкти
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    status = serializers.BooleanField()
    weight = serializers.FloatField()
    def create(self, validated_data:dict):
        user=UserModel.objects.create(**validated_data)
        return user
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
