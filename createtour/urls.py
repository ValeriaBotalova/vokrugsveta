from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.hotels_view, name='hotels')
]
