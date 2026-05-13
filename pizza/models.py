from django.db import models

# Create your models here.
from django.db import models

class PizzaModel(models.Model):
    class Meta:
        db_table = 'pizza'
    name = models.CharField(max_length = 20)
    size = models.IntegerField()
    price = models.FloatField()
