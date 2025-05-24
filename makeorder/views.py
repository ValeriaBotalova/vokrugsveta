from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Rooms, Hotels, Tours, Clients
from datetime import datetime

class OrderCreateView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    
    def get(self, request, room_id):
        room = get_object_or_404(Rooms, id=room_id)
        hotel = room.hotel
        return render(request, 'makeorder/order_create.html', {
            'room': room,
            'hotel': hotel,
            'today': datetime.now().strftime('%Y-%m-%d')
        })
    
    def post(self, request, room_id):
        room = get_object_or_404(Rooms, id=room_id)
        hotel = room.hotel
        
        try:
            arrival_date = request.POST.get('arrival_date')
            departure_date = request.POST.get('departure_date')
            
            if not arrival_date or not departure_date:
                messages.error(request, "Пожалуйста, укажите даты заезда и выезда")
                return redirect('makeorder:order_create', room_id=room_id)
            
            arrival = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            departure = datetime.strptime(departure_date, '%Y-%m-%d').date()
            
            if arrival >= departure:
                messages.error(request, "Дата выезда должна быть позже даты заезда")
                return redirect('makeorder:order_create', room_id=room_id)
            
            client = Clients.objects.get(user=request.user)
            
            tour = Tours.objects.create(
                client=client,
                country=hotel.country,
                arrival_date=arrival,
                departure_date=departure,
                price=room.price * (departure - arrival).days,
                status='pending',
                hotel=hotel
            )
            
            messages.success(request, 
                f"Бронирование №{tour.id} успешно создано! "
                f"Статус: {tour.get_status_display()}")
            return redirect('account:history')
            
        except Exception as e:
            messages.error(request, f"Ошибка при бронировании: {str(e)}")
            return redirect('makeorder:order_create', room_id=room_id)