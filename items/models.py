from django.db import models


class Item (models.Model):
    uuid = models.UUIDField()
    pics = [models.URLField()]
    description = models.CharField(max_length=500)
    price = models.FloatField()
    owner = models.UUIDField()
    isSold = models.BooleanField()

# Create your models here.
