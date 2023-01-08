import os
import re
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *
from django.contrib.auth.hashers import make_password, check_password

from django.core.signing import Signer
import base64

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        print(e)
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

def dashboard(request):
    return render(request, 'index.html')


def menu(request):
    return render(request, 'Menu.html')


def roles(request):
    #role = Roles.objects.values('id','role')
    role = Roles.objects.all()
   # role = Roles.objects.raw("SELECT * FROM dashboard_roles ORDER BY role")
    l = []

    for i in role:
        # i['encrypt_id'] = encrypt(i['id'])
        # i['id'] = i['id']
        i.encrypt_id = encrypt(i.id)
        i.id=i.id

        l.append(i)

    print(l)
    return render(request, 'roles.html',{'role':l})

def view_role(request,pk):
    pk = decrypt(pk)
    try:
        role = Roles.objects.get(id=pk)
        return render(request, 'view_role.html', {'role': role})
    except(Exception):
        return render(request, 'pagenotfound.html', {'e': Exception})

def roles_report(request):
    role = Roles.objects.all()
    return render(request, 'role_report.html', {'role':role})
def pagenotfound(request):
    return render(request, 'pagenotfound.html')


def pdf_report_create(request):
    role = Roles.objects.all()
    template_path = 'pdf_report.html'
    context = {'role': role}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="roles_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def role_mail_template(request,pk):
    pk = decrypt(pk)
    try:
        role = Roles.objects.get(id=pk)
        html_content = render_to_string('role_mail_template.html', {'role': role})
        text_content = strip_tags(html_content) #remove html tags
        email = EmailMultiAlternatives(
            #subject
            "News",
            #content
            text_content,
            #from
           'admin@HFMS.com',
            #to
            ['sidraparacha27@gmail.com', 'sidrapa27@gmail.com']
        )

        email.attach_alternative(html_content,"text/html")
        email.send()

        return render(request, 'role_mail_template.html', {'role': role})
    except(Exception):
        return HttpResponse("Couldn't send email")


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
    pk = decrypt(pk)
    role = Roles.objects.filter(id=pk)
    role.delete()
    messages.success(request, "Role deleted!")
    return redirect('/dashboard/roles')

# USERS
# def register(request):
#     role = Roles.objects.filter(role="Customer")
#     return render(request, 'register.html', {'role': role})

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
    cat = Categories.objects.all()
    catObj = Categories()
    strId = str(catObj.id)
    encryptId=make_password(strId)
    #encryptId=crypt.crypt(strId)
    decryptId = check_password(strId, encryptId)
    signer = Signer()
    # encrypt_key = signer.sign_object(catObj.id)
    # decrypt_key = signer.unsign_object(encrypt_key)

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
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id==2:
            return render(request, 'categories.html',{'cat':cat,'encryptId':encryptId,'decryptId':decryptId})
        else:
            return redirect('../website/index')
    else:
        return redirect('../website/login')

    # return render(request,'categories.html',{'cat':cat})

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
    # signer = Signer()
    # decrypt_key = signer.unsign_object(pk)
    catObj = Categories()
    strId = str(catObj.id)
    decryptId = check_password(strId, pk)
    cat = Categories.objects.get(id=decryptId)

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