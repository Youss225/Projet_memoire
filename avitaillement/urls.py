from django.urls import path
from .views import page_avitaillement, stocks_page

urlpatterns = [
    path("", page_avitaillement, name="avitaillement"),
    path("stocks/", stocks_page, name="stocks"),
]