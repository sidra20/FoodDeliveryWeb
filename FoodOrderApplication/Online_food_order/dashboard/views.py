import re

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Roles


# Create your views here.

def index(request):

    return render(request, 'index.html')


def menu(request):
    return render(request, 'Menu.html')


def roles(request):
    role = Roles.objects.all()
    return render(request, 'roles.html',{'role':role})


def role_store(request):
    rolesObj = Roles()

    roles = request.POST.get('role')
    rolesObj.role = roles
    if not request.POST.get('role'):
        messages.error(request, "The fields are required!")

    if not re.match(r'^[A-Za-z]{3,50}$', request.POST.get('role')):
        messages.error(request, "Incorrect format!")

    else:
        if Roles.objects.filter(role=roles):
            messages.error(request, "Already exists!")
        else:
            rolesObj.save()
            messages.success(request, "Role added!")

    # for list in role_list:
    #     if(list.role == request.POST.get('role')):
    #         messages.error(request, "Role alreday exists!")
    #     else:
    #         role.save()
    #         messages.success(request, "Role added!")

    return redirect('/dashboard/roles')

def delete_role(request,pk):
    role = Roles.objects.filter(id=pk)
    role.delete()
    messages.success(request, "Role deleted!")
    return redirect('/dashboard/roles')