from django.shortcuts import render
import json
from django.http import HttpResponse
from user.models import User
from items.models import Item
from order.models import Order
from .models import Bill
from .models import Delivery
import uuid
import logging
from django.contrib.auth import authenticate


def pay(request):
    newbill = Bill.objects.__new__()
    order = Order.objects.get(UUID=request.POST.get('uuid'))
    newbill.UUID = uuid.uuid4()
    newbill.type = request.POST.get('type')
    if newbill.type == 0:
        newbill.payment = 'offline'
    else:
        newbill.payment = request.POST.get('payment')
    newbill.price = order.value
    newbill.save()
    order.save()
    return HttpResponse(newbill.uuid, status=201)


def getbill(request):
    bill = Bill.objects.get(UUID=request.GET.get('uuid'))
    return HttpResponse(bill.payment, status=200)


def adddelivery(request):
    delivery = Delivery.objects.__new__()
    order = Order.objects.get(UUID=request.POST.get('uuid'))
    delivery.UUID = uuid.uuid4()
    if request.POST.get('type') == 'offline':
        delivery.type = 0
        delivery.positions.append('面交')
    else:
        delivery.type = 1
        delivery.positions.append('已发货')
    delivery.save()
    order.delivery = delivery.UUID
    order.save()
    return HttpResponse(status=201)


def updatedelivery(request):
    delivery = Delivery.objects.get(UUID=request.POST.get('uuid'))
    delivery.positions.append(request.POST.get('position'))
    delivery.save()
    return HttpResponse(status=200)


def getdelivery(request):
    delivery = Delivery.objects.get(UUID=request.GET.get('uuid'))
    rep = {
        'position': delivery.positions
    }
    return HttpResponse(json.dumps(rep), status=200)

# Create your views here.
