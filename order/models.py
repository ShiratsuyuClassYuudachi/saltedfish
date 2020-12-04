from django.db import models


class Order(models.Model):
    UUID = models.UUIDField(),
    itemId = models.UUIDField(),
    seller = models.UUIDField(),
    buyer = models.UUIDField(),
    value = models.FloatField(),
    time = models.TimeField(),
    check = models.UUIDField(),
    buyerComment = models.CharField(max_length=500),
    sellerComment = models.CharField(max_length=500)
# Create your models here.
