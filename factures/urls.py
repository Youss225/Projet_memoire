from django.urls import path
from .views import factures_page, facture_pdf, facture_preview

urlpatterns = [
    path('', factures_page),
    path('<int:id>/preview/', facture_preview),
    path('<int:id>/pdf/', facture_pdf),
]