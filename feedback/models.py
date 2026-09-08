from django.db import models
from django.utils import timezone


class Feedback(models.Model):

    TYPE_MESSAGE = [
        ("SAT", "Satisfaction"),
        ("REC", "Réclamation"),
        ("SUG", "Suggestion"),
        ("INC", "Incident"),
    ]

    nom = models.CharField(
        max_length=100
    )

    entreprise = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    telephone = models.CharField(
        max_length=30,
        blank=True
    )

    type_message = models.CharField(
        max_length=3,
        choices=TYPE_MESSAGE
    )

    sujet = models.CharField(
        max_length=200
    )

    message = models.TextField()

    note = models.PositiveSmallIntegerField(
        default=5
    )

    # Gestion commerciale
    lu = models.BooleanField(
        default=False
    )

    traite = models.BooleanField(
        default=False
    )

    reponse = models.TextField(
        blank=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_reponse = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.nom} - {self.get_type_message_display()}"

    def enregistrer_reponse(self, texte):
        self.reponse = texte
        self.traite = True
        self.date_reponse = timezone.now()
        self.save()