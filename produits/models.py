from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


# ======================
# PRODUIT
# ======================

class Produit(models.Model):

    nom = models.CharField(
        max_length=100
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.nom


# ======================
# CREATION AUTOMATIQUE DU STOCK
# ======================

@receiver(post_save, sender=Produit)
def creer_stock_auto(sender, instance, created, **kwargs):

    if created:

        StockCuve = apps.get_model(
            "avitaillement",
            "StockCuve"
        )

        StockCuve.objects.get_or_create(
            produit=instance,
            defaults={
                "capacite_totale": 100000,
                "stock_actuel": 100000,
                "seuil_alerte": 1000
            }
        )