from django.urls import path
from .views import feedback_page, feedback_inbox

urlpatterns = [
    path("", feedback_page, name="feedback"),
    path("inbox/", feedback_inbox, name="feedback_inbox"),
]