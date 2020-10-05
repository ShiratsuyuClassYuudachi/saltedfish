from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.contrib.auth.admin import User
import time
import uuid
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def index(request):
    return HttpResponse("Hello,world")


def register(request):
    model = User()
    return HttpResponse(request.POST.get('account'), status=201)
    ''' model.account = request.POST.get('account')
    model.name = request.POST.get('name')
    model.email = request.POST.get('email')
    model.password = request.POST.get('password')
    model.uuid = uuid.uuid1()
    model.joinDate = time.localtime()
    try:
        model.save()
    except:
        logging.log("Saving error")
        return HttpResponse(status=500)
    return HttpResponse(request.POST.get('account'), status=201)'''


def information(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.last_login)
    else:
        return HttpResponse("unauthenticated",status=401)

# Create your views here.
