from django.shortcuts import render
from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


def feedback_page(request):
    return render(request, "feedback.html")


def feedback_inbox(request):
    return render(request, "inbox_feedback.html")