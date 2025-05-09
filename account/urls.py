from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_view, name='data'),
    path('history', views.history_view, name='history')
]
