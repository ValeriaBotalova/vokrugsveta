from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from core.models import Tours
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("TEST OK")

class AdminToursView(UserPassesTestMixin, View):
    template_name = 'admin_panel/tour_list.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get(self, request):
        tours = Tours.objects.all().order_by('-arrival_date')
        print(f"Найдено туров: {tours.count()}") 
        return render(request, self.template_name, {'tours': tours})


class ProcessTourView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
    def post(self, request, tour_id):
        tour = Tours.objects.get(id=tour_id)
        action = request.POST.get('action')
        
        if action == 'confirm':
            tour.status = 'confirmed'
        elif action == 'admin_cancel':
            tour.status = 'canceled'
        
        tour.save()
        return redirect('admin_panel:list')