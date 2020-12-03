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
            UUID = uuid.uuid4()
            new_item = Item(description=description, pics=pics, price=price, owner=owner, isSold=isSold, UUID=UUID)
            new_item.save()
            return HttpResponse(UUID)
    return HttpResponse("unauthenticated", status=401)


def get(request):
    itemid = request.GET.get('uuid')
    try:
        item = Item.objects.get(UUID=itemid)
    except Exception:
        HttpResponse("No such item", status='404')
    else:
        rep = {
            'pics': item.pics,
            'description': item.description,
            'price': item.price,
            'owner': item.owner
        }
        return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def getList(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    itemlist = Item.objects.all()[offset:(limit+offset)]
    uuidlist = []
    for item in itemlist:
        uuidlist.append(item.UUID)
    rep = {
        'length': len(itemlist),
        'list': uuidlist
    }
    return HttpResponse(json.dumps(rep),content_type="application/json", status=200)

# Create your views here.
