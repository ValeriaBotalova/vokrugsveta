from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Tours, Clients

class HistoryView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    
    def get(self, request):
            client = Clients.objects.get(user=request.user)
            tours = Tours.objects.filter(client=client).order_by('-arrival_date')
            
            countries = set(tour.hotel.country for tour in tours if tour.hotel and tour.hotel.country)
            
            context = {
                'tours': tours,
                'tours_count': tours.count(),
                'countries_count': len(countries),
            }
            return render(request, 'account/history.html', context)

def logout_view(request):
    logout(request)
    return render(request,'main/mainpage.html')
