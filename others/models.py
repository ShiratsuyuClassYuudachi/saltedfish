from django.db import models


class bill(models.Model):
    UUID = models.UUIDField(),
    price = models.FloatField(),
    type = models.IntegerField(),
    payment = models.CharField()


class delivery(models.Model):
    UUID = models.UUIDField(),
    type = models.IntegerField(),
    positions = [models.CharField(max_length=500)]

# Create your models here.
