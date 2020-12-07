from django.urls import path

from . import views

urlpatterns = [
    path('send', views.send),
    path('getlist', views.getlist),
    path('getdetail', views.getdetial),
    path('getmessage', views.getmessage)
]
