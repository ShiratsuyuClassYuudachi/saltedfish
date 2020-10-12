from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from user.models import User
import time
import uuid
import logging
from django.contrib import auth
from django.contrib.auth import authenticate


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
        User.objects.create_user(username=username, password=password, email=email, uuid=uuid.uuid1())
        user = authenticate(email=email, password=password)
        request.session['uuid'] = str(user.uuid)
    except:
        logging.log("Saving error")
        return HttpResponse(status=500)
    return HttpResponse(request.POST.get('account'), status=200)


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


def information(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            return HttpResponse(request.user.username)
    return HttpResponse("unauthenticated", status=401)

# Create your views here.
