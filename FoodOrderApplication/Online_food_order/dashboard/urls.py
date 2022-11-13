from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index),
    path('menu', views.menu),
    path('roles', views.roles),
    path('roles_store', views.role_store),
    path('role_delete/<int:pk>', views.delete_role, name="deleteRole"),
    path('register', views.register),
    path('register_store', views.register_store),

]