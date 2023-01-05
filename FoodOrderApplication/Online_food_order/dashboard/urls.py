from django.urls import path

from . import views

urlpatterns = [
    path('home', views.dashboard),
    path('menu', views.menu),
    path('roles', views.roles),
    path('roles_store', views.role_store),
    path('role_delete/<str:pk>', views.delete_role, name="deleteRole"),
    path('role_view/<str:pk>', views.view_role, name="viewRole"),
    path('register_store', views.register_store),
    path('categories', views.category_index),
    path('category_store', views.category_store),
    path('category_delete/<int:pk>', views.category_delete, name="deleteCategory"),
    path('category_edit/<str:pk>', views.category_edit),
    path('category_update', views.category_update),

]