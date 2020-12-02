from django.contrib.auth.base_user import AbstractBaseUser
from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    _id=models.ObjectIdField()
    uuid = models.UUIDField()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=False)
    itemToSell = [models.UUIDField()]
    soldItem = [models.UUIDField()]
    boughtItem = [models.UUIDField()]
    wishList = [models.UUIDField()]
    avatar = models.URLField
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    pass
# Create your models here.
