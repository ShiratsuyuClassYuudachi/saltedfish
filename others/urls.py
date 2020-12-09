from django.urls import path

from . import views

urlpatterns = [
    path('pay', views.pay),
    path('getbill', views.getbill),
    path('adddelivery', views.adddelivery),
    path('updatedelivery', views.updatedelivery),
    path('getdelivery', views.getdelivery)
]
