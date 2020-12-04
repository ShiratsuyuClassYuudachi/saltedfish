from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add, name='add'),
    path('get', views.get),
    path('getlist', views.getList),
    path('search', views.search)
]
