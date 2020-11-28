from django.shortcuts import render
import json
from django.http import HttpResponse
from user.models import User
from items.models import Item
import uuid
import logging
from django.contrib.auth import authenticate


def add(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            data = json.load(request.body)
            description = data.description
            pics = data.pics
            price = data.price
            owner = uuid.UUID(request.session.get("uuid"))
            isSold = False
            UUID=uuid.uuid4()
            new_item = Item(description=description,pics=pics,price=price,owner=owner,isSold=isSold,UUID=UUID)
            new_item.save()
            return HttpResponse(UUID)


# Create your views here.
