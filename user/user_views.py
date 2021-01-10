# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
import sys

@login_required
def profile(request):
    context={}
    return render(request,'change_password.html',context)

@user_passes_test(lambda u: u.is_superuser)
def list(request):
    page="user"
    User = get_user_model()
    user = User.objects.all()
    context={"page":page,"list_user":user}
    return render(request,'user_list.html',context)


@user_passes_test(lambda u: u.is_superuser)
def create(request):
    page="user"
    context={"page":page}
    return render(request,'user_create.html',context)

@user_passes_test(lambda u: u.is_superuser)
def edit(request,id):
    page="user"
    User = get_user_model()
    user = User.objects.get(pk=id)
    
    context={"page":page,"user":user}
    return render(request,'user_edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def save(request):
    page="user"
    context={"page":page}
    
    email  =request.POST.get("email","")

    password  =request.POST.get("password","")

    chk_is_active = request.POST.get("chk_is_active",False)

    chk_is_superuser = request.POST.get("chk_is_superuser",False)

    is_active= False
    if(chk_is_active):
        is_active = True

    # is_superuser= False

    # if(chk_is_superuser):
    #     is_superuser = True
    is_superuser = True

    try:
        User = get_user_model()
        user = User.objects.create_user(
                email=email,is_active=is_active,is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.INFO, 'Create New User Success ')
        return HttpResponseRedirect(reverse('user:list'))
    except:
        t, v, tb = sys.exc_info()
        messages.add_message(request, messages.ERROR, ' Error Create New User')
        return render(request,'user_create.html',context)
        

    


@user_passes_test(lambda u: u.is_superuser)
def update(request,id):
    page="user"
    context={"page":page}
    User = get_user_model()
    user = User.objects.get(pk=id)
    email  =request.POST.get("email","")
    chk_is_superuser = request.POST.get("chk_is_superuser",False)

    chk_is_active = request.POST.get("chk_is_active",False)

    
    


    is_active= False
    # is_superuser = False

    if(chk_is_active):
        is_active = True
    
    # if(chk_is_superuser):
    #     is_superuser = True
    is_superuser = True

    try:
        user.email = email
        user.is_active=is_active
        user.is_superuser=is_superuser
        user.save()
        password  =request.POST.get("password","")
        if(password != ""):
            user.set_password(password)
        messages.add_message(request, messages.INFO, 'Update  User Success ')
        return HttpResponseRedirect(reverse('user:list'))
    except:
        t, v, tb = sys.exc_info()
        messages.add_message(request, messages.ERROR, ' Error Update New User  %s' % (v))
        return HttpResponseRedirect(reverse('user:edit',kwargs={'id':id}))



@user_passes_test(lambda u: u.is_superuser)
def delete(request,id):
    page="user"
    context={"page":page}
    try:
        User = get_user_model()
        User.objects.filter(pk=id).delete()
        messages.add_message(request, messages.INFO, 'Delete  User Success ')
    except:
        t, v, tb = sys.exc_info()
        messages.add_message(request, messages.ERROR, ' Error Delete  User  %s' % (v))
    return HttpResponseRedirect(reverse('user:list'))



@login_required
def changepassword(request):
    context={}
    if request.method == 'POST':
        user = request.user
        success = user.check_password(request.POST['password'])
        if(success):
            #Change password
            messages.add_message(request, messages.INFO, 'Change password success')
            user.set_password(request.POST['new_password'])
            user.save()
            return HttpResponseRedirect(reverse('user:profile'))

        else:
            #Current password is wrong 
            messages.add_message(request, messages.ERROR, 'Current password is wrong')
            return HttpResponseRedirect(reverse('user:profile'))

    return HttpResponseRedirect(reverse('user:profile'))

    
    


def login(request):
    context={}
    if request.POST:
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.INFO, 'Login Success ')
            return HttpResponseRedirect(reverse('user:list'))
            
        else:
            messages.add_message(request, messages.ERROR, 'Email or Password is not correct or inactive')
            context={}


    return render(request,'signin.html',context)

def signout(request):
    context={}
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))
