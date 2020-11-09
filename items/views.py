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
        Item.
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            data = json.load(request.body)
            description = data.description
            pics = data.pics
            price = data.price
            owner = uuid.UUID(request.session.get("uuid"))
            isSold = False
            uuid.uuid4()


# Create your views here.
