from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
]
