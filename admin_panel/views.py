from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from core.models import Tours
from django.http import HttpResponse
from django.template.loader import render_to_string
from openpyxl import Workbook
from io import BytesIO

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

class ExportToursView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, format_type):
        tours = Tours.objects.all().order_by('-arrival_date')
        
        if format_type == 'xlsx':
            return self.export_xlsx(tours)
        elif format_type == 'html':
            return self.export_html(tours)
        else:
            return HttpResponse("Unsupported format", status=400)

    def export_xlsx(self, tours):
        wb = Workbook()
        ws = wb.active
        ws.title = "Tours"

        headers = ["ID", "Клиент", "Отель", "Дата прибытия", "Дата выезда", "Статус"]
        ws.append(headers)

        for tour in tours:
            # Получаем полное имя через связанного пользователя
            client_name = f"{tour.client.user.first_name} {tour.client.user.last_name}".strip()
            if not client_name:  # Если имя и фамилия не заполнены
                client_name = str(tour.client.user)
                
            ws.append([
                tour.id,
                client_name,  # Исправленная строка
                str(tour.hotel.name),
                tour.arrival_date,
                tour.departure_date,
                tour.get_status_display()
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="tours_export.xlsx"'
        return response

    def export_html(self, tours):
        html = render_to_string('admin_panel/tours_export.html', {'tours': tours})
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="tours_export.html"'
        return response