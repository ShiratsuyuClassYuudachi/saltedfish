from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from user.models import User
import time
import uuid
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def index(request):
    return HttpResponse("Hello,world")


def register(request):
    username = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    Uuid = uuid.uuid1()
    try:
        user = User.objects.create()
        user.password = password
        user.username = username
        user.email = email
        user.uuid = Uuid
        user.save()
    except:
        logging.log("Saving error")
        return HttpResponse(status=500)
    return HttpResponse(request.POST.get('account'), status=201)


def information(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.last_login)
    else:
        return HttpResponse("unauthenticated", status=401)

# Create your views here.
