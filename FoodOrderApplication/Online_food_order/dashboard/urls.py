from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index),
    path('menu', views.menu),
]