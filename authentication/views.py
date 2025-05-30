from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Clients
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.db import IntegrityError
from django.core.exceptions import ValidationError


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

class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    success_url = reverse_lazy('password_reset')
    email_template_name = 'authentication/password_reset_email.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['reset_done'] = True
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['done'] = self.request.session.pop('reset_done', False)
        context['subject'] = "Восстановление пароля"
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_confirm')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['reset_complete'] = True
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['done'] = self.request.session.pop('reset_complete', False)
        return context

User = get_user_model()

def registration_view(request):
    context = {}
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']
            lastname = request.POST['lastname']
            birthdate = request.POST.get('birthdate')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')

            if not all([email, password, name, lastname, birthdate, phone, gender]):
                raise ValueError("Заполните все обязательные поля.")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
                last_name=lastname
            )

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            Clients.objects.create(
                user=user,
                first_name=name,
                last_name=lastname,
                date_of_birth=birthdate,
                phone=phone,
                email=email,
                gender=gender
            )

            login(request, user)
            return redirect('history')

        except IntegrityError as e:
            context['error_message'] = 'Ошибка базы данных: ' + str(e)
        except ValidationError as e:
            context['error_message'] = 'Ошибка валидации: ' + str(e)
        except Exception as e:
            context['error_message'] = 'Ошибка регистрации: ' + str(e)
            if 'user' in locals() and user.id:
                user.delete()

    return render(request, 'authentication/registration.html', context)
    
def password_reset_confirm(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 and new_password2:
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, "Пароль успешно изменен. Можете войти.")
                    return redirect('history') 
                else:
                    messages.error(request, "Пароли не совпадают.")
            else:
                messages.error(request, "Пожалуйста, заполните все поля.")
        return render(request, 'authentication/password_reset_confirm.html', {
            'validlink': True,
        })
    else:
        return render(request, 'authentication/password_reset_confirm.html', {
            'validlink': False,
        })
