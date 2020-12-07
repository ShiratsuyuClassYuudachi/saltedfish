from django.urls import path

from . import views

urlpatterns = [
    path('buy', views.buy),
    path('cancel', views.cancel),
    path('confirm', views.confirm),
    path('comment', views.comment),
    path('getscore', views.gstScore),
    path('info', views.info)
]
