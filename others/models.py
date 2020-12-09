from django.db import models


class Bill(models.Model):
    UUID = models.UUIDField(),
    price = models.FloatField(),
    type = models.IntegerField(),
    payment = models.CharField(max_length=128)


class Delivery(models.Model):
    UUID = models.UUIDField(),
    type = models.IntegerField(),
    positions = [models.CharField(max_length=500)]

# Create your models here.
