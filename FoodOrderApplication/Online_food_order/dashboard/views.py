import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.

def dashboard(request):

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

    if not re.match(r'^[A-Za-z ]{3,50}$', request.POST.get('role')):
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

# USERS
def register(request):
    role = Roles.objects.filter(role="Customer")
    return render(request, 'register.html', {'role': role})

def register_store(request):
    usersObj = Users()
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    cpass = request.POST.get('cpass')
    userrole = request.POST.get('role')
    today = date.today()
    d = today.strftime("%d/%m/%Y")



    usersObj.name=name
    usersObj.email=email
    usersObj.password=make_password(password)
    usersObj.date=d
    usersObj.role_id=userrole

    if not name:
        messages.error(request, "The fields are required!")
    elif not email:
        messages.error(request, "The fields are required!")
    elif not password:
        messages.error(request, "The fields are required!")
    elif not cpass:
        messages.error(request, "The fields are required!")
    elif not userrole:
        messages.error(request, "The fields are required!")

    else:
        if len(name)<3:
            messages.error(request, "Name shouldn't be less than 3 characters.")
        if len(password)<6:
            messages.error(request, "Password shouldn't be less than 6 characters.")

        else:
            if password != cpass:
                messages.error(request, "Password do not match.")
            elif not re.match(r'^[A-Za-z ]{3,150}$', name):
                messages.error(request, "Name is not correct in format!")
            elif not re.match(r'^[A-Za-z]{1,15}[0-9@#$%&*^!]{1,15}$', password):
                messages.error(request, "Password should contain numbers or special charater!")
            elif Users.objects.filter(email=email):
                messages.error(request, "Email already exists!")
            else:
                usersObj.save()
                messages.success(request,"Registered successfully!")
    return redirect('../website/register')