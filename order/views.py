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
            if Item.objects.filter(UUID=request.POST.get('item')).exists():
                item = Item.objects.get(UUID=(request.POST.get('item')))
                order = Order.objects.__new__()
                order.UUID = uuid.uuid4()
                order.time = time.time()
                order.itemId = item.UUID
                order.buyer = uuid.UUID(request.session.get("uuid"))
                order.seller = item.owner
                order.value = item.price
                order.paid = False
                order.finished = False
                order.buyerScore = -1
                order.sellerScore = -1
                order.save()
                seller = User.objects.get(uuid=item.owner)
                seller.itemToSell.remove(item.UUID)
                return HttpResponse(status=201)
            return HttpResponse(status=404)
    return HttpResponse(status=401)


def cancel(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            if Order.objects.filter(UUID=request.POST.get('order')).exists():
                order = Order.objects.get(UUID=request.POST.get('order'))
                if user is order.seller | user is order.buyer:
                    if order.paid is False:
                        seller = User.objects.get(uuid=order.seller)
                        seller.itemToSell.append(order.UUID)
                        order.delete()
                        return HttpResponse(status=200)
                    return HttpResponse(status=403)
                return HttpResponse(status=404)
    return HttpResponse(status=401)


def info(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            if Order.objects.filter(UUID=request.POST.get('order')).exists():
                order = Order.objects.get(UUID=request.POST.get('order'))
                if user is order.seller | user is order.buyer:
                    if order.paid is False:
                        rep = {
                            'status': 'unpaid',
                            'item': order.itemId,
                            'time': order.time,
                            'value': order.value,
                            'buyer': order.buyer,
                            'seller': order.seller
                        }
                        return HttpResponse(json.dumps(rep), status=200)
                    else:
                        if order.finished is False:
                            rep = {
                                'status': 'paid',
                                'item': order.itemId,
                                'value': order.value,
                                'time': order.time,
                                'buyer': order.buyer,
                                'seller': order.seller,
                                'delivery': order.delivery
                            }
                            return HttpResponse(json.dumps(rep), status=200)
                        else:
                            if order.sellerScore != -1 | order.buyerScore == -1:
                                rep = {
                                    'status': 'seller_scored',
                                    'item': order.itemId,
                                    'value': order.value,
                                    'time': order.time,
                                    'buyer': order.buyer,
                                    'seller': order.seller,
                                    'delivery': order.delivery,
                                    'sellerScore': order.sellerScore,
                                    'sellerComment': order.sellerComment
                                }
                                return HttpResponse(json.dumps(rep), status=200)
                            elif order.sellerScore == -1 | order.buyerScore != -1:
                                rep = {
                                    'status': 'buyer_scored',
                                    'item': order.itemId,
                                    'value': order.value,
                                    'time': order.time,
                                    'buyer': order.buyer,
                                    'seller': order.seller,
                                    'delivery': order.delivery,
                                    'buyerScore': order.buyerScore,
                                    'buyerComment': order.buyerComment
                                }
                                return HttpResponse(json.dumps(rep), status=200)
                            elif order.sellerScore != -1 & order.buyerScore != -1:
                                rep = {
                                    'status': 'both_scored',
                                    'item': order.itemId,
                                    'value': order.value,
                                    'time': order.time,
                                    'buyer': order.buyer,
                                    'seller': order.seller,
                                    'delivery': order.delivery,
                                    'buyerScore': order.buyerScore,
                                    'buyerComment': order.buyerComment,
                                    'sellerScore': order.sellerScore,
                                    'sellerComment': order.sellerComment
                                }
                                return HttpResponse(json.dumps(rep), status=200)
                            else:
                                rep = {
                                    'status': 'finished',
                                    'item': order.itemId,
                                    'value': order.value,
                                    'time': order.time,
                                    'buyer': order.buyer,
                                    'seller': order.seller,
                                    'delivery': order.delivery,
                                }
                                return HttpResponse(json.dumps(rep), status=200)
                return HttpResponse(status=403)
            return HttpResponse(status=404)
    return HttpResponse(status=401)


def confirm(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            if Order.objects.filter(UUID=request.POST.get('order')).exists():
                order = Order.objects.get(UUID=request.POST.get('order'))
                if order.paid is True and order.finished is False:
                    if user == order.buyer:
                        order.finished = True
                        order.save()
                        seller = User.objects.get(uuid=order.seller)
                        seller.soldItem.append(order.UUID)
                        buyer = User.objects.get(uuid=order.buyer)
                        buyer.boughtItem.append(order.UUID)
                        return HttpResponse(status=200)
                    return HttpResponse(status=403)
                return HttpResponse(status=403)
            return HttpResponse(status=404)
    return HttpResponse(status=401)


def gstScore(request):
    user = request.GET.get('user')
    order = Order.objects.get(UUID=request.GET.get('order'))
    if order.finished is True:
        if user is order.buyer:
            if order.sellerScore != -1:
                rep = {
                    'status': 'scored',
                    'score': order.sellerScore,
                    'comment': order.sellerComment
                }
                HttpResponse(json.dumps(rep), status=200)
            else:
                rep = {
                    'status': 'finished',
                }
                HttpResponse(json.dumps(rep), status=200)
        elif user is order.seller:
            if order.buyerScore != -1:
                rep = {
                    'status': 'scored',
                    'score': order.buyerScore,
                    'comment': order.buyerComment
                }
                HttpResponse(json.dumps(rep), status=200)
            else:
                rep = {
                    'status': 'finished',
                }
                HttpResponse(json.dumps(rep), status=200)
        return HttpResponse(status=412)
    return HttpResponse(status=403)


def comment(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.uuid.UUID(request.session.get("uuid"))
            order = Order.objects.get(UUID=request.POST.get('order'))
            if user == Order.buyer:
                if order.buyerScore == -1:
                    order.buyerScore = request.POST.get('score')
                    order.buyerComment = request.POST.get('comment')
                    order.save()
                    return HttpResponse(status=201)
                else:
                    return HttpResponse('scored', status=403)
            elif user == order.seller:
                if order.sellerScore == -1:
                    order.sellerScore = request.POST.get('score')
                    order.sellerComment = request.POST.get('comment')
                    return HttpResponse(status=201)
                return HttpResponse('scored', status=403)
            else:
                return HttpResponse('no auth', status=403)
    return HttpResponse(status=401)

# Create your views here.
