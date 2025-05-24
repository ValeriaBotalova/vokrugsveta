from django.urls import path
from . import views
from .views import HistoryView

urlpatterns = [
    path('history/', HistoryView.as_view(), name='history'),
    path('logout/', views.logout_view, name='logout'),
]
