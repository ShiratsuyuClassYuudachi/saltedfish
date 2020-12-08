import json
import logging
import uuid

from django.contrib.auth import authenticate
from django.http import HttpResponse

from user.models import User


def index(request):
    return HttpResponse("Hello,world")


def register(request):
    username = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if User.objects.filter(email=email).exists():
        return HttpResponse("This email has been used", status=401)
    if User.objects.filter(username=username).exists():
        return HttpResponse("This username has been used", status=401)
    try:
        User.objects.create_user(username=username, password=password, email=email, uuid=uuid.uuid4())
        user = authenticate(email=email, password=password)
        request.session['uuid'] = str(user.uuid)
    except:
        logging.log("Saving error")
        return HttpResponse(status=500)
    return HttpResponse(request.POST.get('email'), status=201)


def login(request):
    email = request.POST.get('email')
    password = str(request.POST.get('password'))
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            return HttpResponse(status=304)
    if not User.objects.filter(email=email).exists():
        return HttpResponse("This email is not used", status=401)
    user = authenticate(request, email=email, password=password)
    if user is not None:
        request.session['uuid'] = str(user.uuid)
        return HttpResponse("Logged in", status=200)
    else:
        return HttpResponse("Password error", status=401)


def setAvatar(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            avatar = request.POST.get('avatar')
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            user.avatar = avatar
            user.save()
            return HttpResponse(status=200)
    return HttpResponse(status=401)


def updateUser(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            username = request.POST.get('username')
            email = request.POST.get('email')
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            user.username = username
            user.email = email
            user.save()
            return HttpResponse(status=200)
    return HttpResponse(status=401)


def changePassword(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            password = request.POST.get('password')
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            user.set_password(password)
            user.save()
            return HttpResponse(status=200)
    return HttpResponse(status=401)


def information(request):

    user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
    rep = {
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def getuuid(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            return HttpResponse(user, status=200)
    return HttpResponse("unauthenticated", status=401)


def toSale(request):
    user = User.objects.get(uuid = request.GET.get('uuid'))
    rep = {
        'list': user.itemToSell
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def sold(request):
    user = User.objects.get(uuid=request.GET.get('uuid'))
    rep = {
        'list': user.soldItem
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def bought(request):
    user = User.objects.get(uuid=request.GET.get('uuid'))
    rep = {
        'list': user.boughtItem
    }
    return HttpResponse(json.dumps(rep), content_type="application/json", status=200)


def wishlist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            rep = {
                'list': user.wishList
            }
            return HttpResponse(json.dumps(rep), content_type="application/json", status=200)
    return HttpResponse("unauthenticated", status=401)


def addwishlist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            item = request.POST.get('item')
            if item not in user.wishList:
                user.wishList.append(item)
                user.save()
                return HttpResponse("success", status=201)
            return HttpResponse("exists", status=403)
    return HttpResponse("unauthenticated", status=401)


def removewishlist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            item = request.POST.get('item')
            if item in user.wishList:
                user.wishList.remove(item)
                user.save()
                return HttpResponse("success", status=200)
            return HttpResponse("exists", status=403)
    return HttpResponse("unauthenticated", status=401)


def inwishlist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            item = request.POST.get('item')
            if item in user.wishList:
                return HttpResponse(status=200)
            return HttpResponse(status=404)
    return HttpResponse("unauthenticated", status=401)


def messagelist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            rep = {
                'list': user.messageList
            }
            return HttpResponse(json.dumps(rep), content_type="application/json", status=200)
    return HttpResponse("unauthenticated", status=401)


def deleteMessage(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = User.objects.get(uuid=uuid.UUID(request.session.get("uuid")))
            session = request.POST.get('sessionid')
            if session in user.messageList:
                user.messageList.remove(session)
                return HttpResponse(status=200)
            return HttpResponse(status=404)
    return HttpResponse("unauthenticated", status=401)
# Create your views here.
