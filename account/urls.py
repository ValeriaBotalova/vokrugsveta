from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.history_view, name='history'),
    path('logout/', views.logout_view, name='logout')
]
