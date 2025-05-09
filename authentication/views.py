from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    return render(request, 'authentication/login.html')

def registration_view(request):
    return render(request, 'authentication/registration.html')

