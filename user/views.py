from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import time
import uuid
import logging


def index(request):
    return HttpResponse("Hello,world")


def register(request):
    model = User
    model.account = request.POST['account']
    model.name = request.POST['name']
    model.email = request.POST['email']
    model.password = request.POST['password']
    model.uuid = uuid.uuid1()
    model.joinDate = time.localtime()
    try:
        model.save()
    except:
        logging.log("Saving error")
        return HttpResponse(status=500)
    return HttpResponse(status=201)
# Create your views here.
