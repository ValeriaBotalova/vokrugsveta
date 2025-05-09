from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def data_view(request):
    return render(request, 'account/data.html')

def history_view(request):
    return render(request, 'account/history.html')

