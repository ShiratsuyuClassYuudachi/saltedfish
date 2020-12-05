from django.shortcuts import render
from django.http import HttpResponse
from user.models import User
import time
import uuid
import logging
from django.contrib.auth import authenticate
import json
from order.models import Order
from items.models import Item


def buy(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            item = request.POST.get('item')
            currtime = time.time()
            value = Item.objects.get(UUID__exact=item).price
            buyer = uuid
            seller = Item.objects.get(UUID__exact=item).owner

        return HttpResponse(status=401)
# Create your views here.
