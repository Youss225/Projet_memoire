from django.urls import path
from .views import produits_page

urlpatterns = [
    path('', produits_page),
]