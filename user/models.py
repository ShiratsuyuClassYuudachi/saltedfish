from django.db import models


class User(models.Model):
    account = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    uuid = models.UUIDField()
    joinDate = models.TimeField()
    itemToSell = [models.UUIDField()]
    soldItem = [models.UUIDField()]
    boughtItem = [models.UUIDField()]
    wishList = [models.UUIDField()]

# Create your models here.
