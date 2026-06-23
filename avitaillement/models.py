from django.db import models
from produits.models import Produit


# ==========================
# STOCK CUVE
# ==========================

class StockCuve(models.Model):

    produit = models.OneToOneField(
        Produit,
        on_delete=models.CASCADE,
        related_name="stock"
    )

    capacite_totale = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    stock_actuel = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    seuil_alerte = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=1000
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.produit.nom} - {self.stock_actuel} L"


# ==========================
# AVITAILLEMENT
# ==========================

class Avitaillement(models.Model):

    TYPE_TRANSPORT = [
        ("PIPELINE", "Pipeline"),
        ("BARGE", "Barge"),
        ("CAMION", "Camion"),
        ("CAMIONS", "Camions"),
    ]

    date_operation = models.DateField()

    nom_navire = models.CharField(
        max_length=150
    )

    type_transport = models.CharField(
        max_length=20,
        choices=TYPE_TRANSPORT
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    destination = models.CharField(
        max_length=255
    )

    heure_debut = models.TimeField()

    heure_fin = models.TimeField()

    consignataire = models.CharField(
        max_length=255
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.nom_navire} - "
            f"{self.produit.nom} - "
            f"{self.quantite} L"
        )


