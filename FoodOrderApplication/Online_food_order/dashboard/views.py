import os
import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from .encryption_util import encrypt
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from dashboard.encryption_util import *

from django.core.signing import Signer
import base64


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


#categories index
def category_index(request):
    cat = Categories.objects.values('id','category')
    catObj = Categories()
    signer = Signer()
    # encrypt_key = signer.sign_object(catObj.id)
    # decrypt_key = signer.unsign_object(encrypt_key)
    encrypt_key = base64.b64encode(catObj.id)
    # li=[]
    # for i in cat:
    #     encrypt_key = base64.b64encode(i['id'])
    #     i['id'] = encrypt_key
    #     li.append(i)


    # li=[]
    # for i in cat:
    #     i['encrypt_key'] = encrypt(i['id'])
    #     i['id'] = i['id']
    #     li.append(i)
    return render(request,'categories.html',{'cat':cat,'encrypt_key':encrypt_key})

def category_store(request):
    catList = Categories.objects.all()
    error =""
    success=""
    cat = Categories()
    category = request.POST.get('category')
    img = request.FILES.get('image')

    cat.category = category
    cat.img = img

    if not category:
        error = "Fields are required!"
    if not img:
        error = "Fields are required!"
    elif len(category)<3:
        error = "Must be more than 3 characters."
    elif not re.match(r'^[A-Za-z ]{3,150}$', category):
        error = "Category name should only contain alphabets!"
    elif Categories.objects.filter(category=category):
        error = "Category already exists!"
    else:
        cat.save()
        success="Category added successfully!"

    return render(request,'categories.html',{'success':success,'error':error,'cat':catList})


def category_delete(request,pk):

    cat = Categories.objects.get(id=pk)
    if(len(cat.img)>0):
        os.remove(cat.img.path)
    cat.delete();
    messages.success(request,"Catgorry deleted successfully!")
    return redirect('/dashboard/categories')

def category_edit(request,pk):
    signer = Signer()
    decrypt_key = signer.unsign_object(pk)

    cat = Categories.objects.get(id=decrypt_key)

    return render(request,'category_edit.html',{'cat':cat})

def category_update(request):
    editerror = ""
    catList = Categories.objects.all()
    cat = Categories.objects.get(id=request.POST.get('id'))
    category = request.POST.get('category')
    img = request.FILES.get('image')



    if not category:
        editerror = "Couldn't update.Fields are required!"
    if not img:
        editerror = "Couldn't update.Fields are required!"

    elif not re.match(r'^[A-Za-z ]{3,150}$', category):
        editerror = "Couldn't update. Category nae should only contain alphabets!"


    else:

        if (len(request.FILES.get('image')) != 0):
            if (len(cat.img) > 0):
                os.remove(cat.img.path)
        cat.img = img
        cat.category = category

        cat.save(update_fields=['category','img'])

        messages.success(request, "Catgorry updated successfully!")


    return render(request,'categories.html',{'editerror':editerror,'cat':catList})