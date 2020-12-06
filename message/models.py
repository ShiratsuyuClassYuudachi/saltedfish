from django.db import models


class MessageList(models.Model):
    UUID = models.UUIDField(),
    time = models.TimeField(),
    sender = models.UUIDField(),
    receiver = models.UUIDField(),
    senderRead = models.BooleanField(),
    receiverRead = models.BooleanField(),
    messages = [models.UUIDField()]


class Message(models.Model):
    UUID = models.UUIDField(),
    time = models.TimeField(),
    type = models.IntegerField(),
    content = models.CharField(max_length=500),
    image = models.URLField()
    sender = models.UUIDField()
# Create your models here.
