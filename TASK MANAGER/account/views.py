from django.shortcuts import render, redirect
from .forms import CustomCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import auth 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


# Create your views here.

def register_user(request):
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('login_user')
    return render(request, 'account/register.html',{'form':form})

def login_user(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login_user')
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    auth.logout(request)
    return redirect('login_user')