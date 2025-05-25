from django.urls import path
from .views import AdminToursView, ProcessTourView, ExportToursView

app_name = 'admin_panel'

urlpatterns = [
    path('', AdminToursView.as_view(), name='list'),
    path('process/<int:tour_id>/', ProcessTourView.as_view(), name='process'),
    path('export/<str:format_type>/', ExportToursView.as_view(), name='export'),
]