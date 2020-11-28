from django.db import models


class Item(models.Model):
    UUID = models.UUIDField()
    pics = [models.URLField()]
    description = models.CharField(max_length=500)
    price = models.FloatField()
    owner = models.UUIDField()
    isSold = models.BooleanField()
    REQUIRED_FIELDS = ['uuid', 'price', 'owner']
# Create your models here.
