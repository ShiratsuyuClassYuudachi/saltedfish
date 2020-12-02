from django.shortcuts import render
from images.models import Img
from django.http import HttpResponse
from user.models import User
import uuid


# Create your views here.
def uploadImg(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            img = Img(img_url=request.FILES.get('img'))
            img.save()
            return HttpResponse(img.img_url)
    return HttpResponse("unauthenticated", status=401)