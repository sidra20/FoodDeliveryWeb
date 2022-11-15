import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

import sys, os
sys.path.append(os.path.abspath('../dashboard/models.py'))
from dashboard.models import *


# Create your views here.

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request,'index.html')

def shop(request):
    return render(request,'shop.html')

def foodItem(request):
    return render(request,'fooditem.html')

def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')

def userRegister(request):
     role = Roles.objects.all()
     return render(request,'user_register.html',{'role':role})
