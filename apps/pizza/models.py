from django.db import models

from core.models import BaseModel


# Create your models here.
class PizzaModel(BaseModel):
    class Meta:
        db_table = 'pizzas'
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    price =models.FloatField()
    pizza_shop = models.ForeignKey('pizza_shop.PizzaShopModel', on_delete=models.CASCADE, related_name='pizzas')

