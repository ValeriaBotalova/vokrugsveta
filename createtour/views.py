from django.shortcuts import render
from core.models import Hotels

def hotels_view(request):
    hotels = Hotels.objects.all()
    countries = Hotels.objects.values_list('country', flat=True).distinct().order_by('country')
    context = {
        'hotels': hotels,
        'countries': countries
    }
    return render(request, 'createtour/hotels.html', context)