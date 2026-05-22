from django.db import models

from project_core.models import BaseModel


# Create your models here.
class PizzaModel(BaseModel):
    class Meta:
        db_table = 'pizza'
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.FloatField()


