from django.urls import path

from . import views


urlpatterns = [
    path('about', views.about),
    path('index', views.index),
    path('shop', views.shop),
    path('food', views.foodItem),
    path('cart', views.cart),
    path('checkout', views.checkout),
    path('register', views.userRegister),

]