from django.urls import include, path
from . import views

urlpatterns = [
    path('hotels/', views.hotels_view, name='hotels'),
    path('hotel/<int:hotel_id>/rooms/', views.hotel_rooms, name='rooms'),
]
