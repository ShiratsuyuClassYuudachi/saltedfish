from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('information', views.information, name='information'),
    path('login', views.login, name='login'),
    path('setavatar', views.setAvatar, name='avatar'),
    path('updateuser', views.updateUser, name='update'),
    path('changepasswd', views.changePassword, name='passwd'),
    path('onsale', views.toSale),
    path('sold', views.sold),
    path('bought', views.bought),
    path('wishlist', views.wishlist),
    path('getuuid',views.getuuid),
    path('addwishlist', views.addwishlist),
    path('removewishlist', views.removewishlist),
    path('checkwishlist', views.inwishlist),
    path('messagelist',views.messagelist),
    path('deletemessage',views.deleteMessage)
]
