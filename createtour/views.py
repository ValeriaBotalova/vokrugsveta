from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Hotels, Rooms

@login_required
def hotels_view(request):
    country_filter = request.GET.get('country', '')
    rating_filter = request.GET.get('rating', '')
    
    hotels = Hotels.objects.all()
    
    if country_filter:
        hotels = hotels.filter(country=country_filter)
    
    if rating_filter:
        hotels = hotels.filter(rating__gte=rating_filter)
    
    countries = Hotels.objects.values_list('country', flat=True).distinct()
    
    context = {
        'hotels': hotels,
        'countries': countries,
        'request': request
    }
    return render(request, 'createtour/hotels.html', context)

@login_required
def hotel_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotels, pk=hotel_id)
    rooms_list = Rooms.objects.filter(hotel=hotel).prefetch_related('roomservices_set__service')
    
    context = {
        'hotel': hotel,
        'rooms': rooms_list,
    }
    return render(request, 'createtour/rooms.html', context)
