from django.urls import path
from .views import OrderCreateView

app_name = 'makeorder'

urlpatterns = [
    path('create/<int:room_id>/', OrderCreateView.as_view(), name='order_create'),
]