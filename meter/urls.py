from django.urls import path
from .views import input_data, dashboard

urlpatterns = [
    path('', input_data, name='input_data'),
    path('dashboard/', dashboard, name='dashboard'),
]
