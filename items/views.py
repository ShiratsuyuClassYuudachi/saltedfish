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
            name = data.name
            description = data.description
            pics = data.pics
            price = data.price
            owner = uuid.UUID(request.session.get("uuid"))
            isSold = False
            UUID = uuid.uuid4()
            new_item = Item(name=name, description=description, pics=pics, price=price, owner=owner, isSold=isSold,
                            UUID=UUID)
            new_item.save()
            seller = User.objects.get(uuid=owner)
            seller.itemToSell.append(UUID)
            return HttpResponse(UUID, status=201)
    return HttpResponse("unauthenticated", status=401)


def update(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            data = json.load(request.body)
            item = Item.objects.get(UUID=data.uuid)
            if item.isSold is False & item.owner == uuid.UUID(request.session.get("uuid")):
                item.name = data.name
                item.description = data.description
                item.pics = data.pics
                item.price = data.price
                item.save()
                return HttpResponse(status=200)
            return HttpResponse(status=403)
    return HttpResponse("unauthenticated", status=401)


def delete(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            data = json.load(request.body)
            item = Item.objects.get(UUID=data.uuid)
            if item.isSold is False & item.owner == uuid.UUID(request.session.get("uuid")):
                seller = User.objects.get(uuid=item.owner)
                seller.itemToSell.remove(item.UUID)
                item.delete()
                return HttpResponse(status=200)
            return HttpResponse(status=403)
    return HttpResponse("unauthenticated", status=401)


def get(request):
    itemId = request.GET.get('uuid')
    try:
        item = Item.objects.get(UUID=itemId)
    except Exception:
        HttpResponse("No such item", status='404')
    else:
        rep = {
            'name': item.name,
            'pics': item.pics,
            'description': item.description,
            'price': item.price,
            'owner': item.owner,
            'isSold': item.isSold
        }
        return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def getList(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    itemList = Item.objects.all().filter(isSold=False)[offset:(limit + offset)]
    uuidList = []
    nameList = []
    picList = []
    priceList = []
    for item in itemList:
        uuidList.append(item.UUID)
        nameList.append(item.name)
        picList.append(item.pics[0])
        priceList.append(item.price)
    rep = {
        'length': len(itemList),
        'uuidlist': uuidList,
        'namelist': nameList,
        'picelist': picList,
        'pricelist':priceList
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def search(request):
    key = request.GET.get('key')
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    itemList = Item.objects.filter(isSold=False).get(description__icontains=key).all()[offset:(offset + limit)]
    uuidList = []
    nameList = []
    picList = []
    priceList = []
    for item in itemList:
        uuidList.append(item.UUID)
        nameList.append(item.name)
        picList.append(item.pics[0])
        priceList.append(item.price)
    rep = {
        'length': len(itemList),
        'uuidlist': uuidList,
        'namelist': nameList,
        'picelist': picList,
        'pricelist': priceList
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)
# Create your views here.
