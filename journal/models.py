from django.db import models
from django.contrib.auth.models import User


class JournalActivite(models.Model):

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    module = models.CharField(
        max_length=50,
        default="SYSTEME"
    )

    action = models.CharField(
        max_length=50
    )

    element = models.TextField(
        blank=True,
        default=""
    )

    adresse_ip = models.CharField(
        max_length=100,
        blank=True,
        default="0.0.0.0"
    )

    date_action = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_action"]

    def __str__(self):
        return f"{self.module} - {self.action}"