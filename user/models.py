from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField()
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=40)
    itemToSell = [models.UUIDField()]
    soldItem = [models.UUIDField()]
    boughtItem = [models.UUIDField()]
    wishList = [models.UUIDField()]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    pass
# Create your models here.
