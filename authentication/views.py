from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Clients

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Неверный email или пароль')
    
    return render(request, 'authentication/login.html')

User = get_user_model()

def registration_view(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST['email'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['name'],
                last_name=request.POST['lastname']
            )
            
            Clients.objects.create(
                user=user,
                first_name=request.POST['name'],
                last_name=request.POST['lastname'],
                date_of_birth=request.POST.get('birthdate'),
                phone=request.POST.get('phone'),
                email=request.POST['email'],
                gender=request.POST.get('gender')
            )
            
            from django.contrib.auth import login
            login(request, user)
            
            return redirect('history')
            
        except Exception as e:

            if 'user' in locals() and user.id:
                user.delete()
            return render(request, 'authentication/registration.html', {
                'error': f'Ошибка регистрации: {str(e)}'
            })
    
    return render(request, 'authentication/registration.html')