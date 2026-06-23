from django.urls import path
from .views import page_clients

urlpatterns = [
    path('', page_clients),
]