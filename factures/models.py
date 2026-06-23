from django.db import models
from clients.models import Client
from produits.models import Produit
from datetime import datetime


class Facture(models.Model):
    reference = models.CharField(max_length=100, unique=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    date_livraison = models.DateField(null=True, blank=True)
    date_limite = models.DateField(null=True, blank=True)

    total = models.FloatField(default=0)

    def save(self, *args, **kwargs):

        if not self.reference:
            annee = datetime.now().year

            dernier = Facture.objects.filter(
                reference__startswith=f"PD-{annee}-"
            ).order_by('-id').first()

            if dernier:
                numero = int(dernier.reference.split("-")[-1]) + 1
            else:
                numero = 1

            self.reference = f"PD-{annee}-{numero:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference


class LigneFacture(models.Model):
    facture = models.ForeignKey(
        Facture,
        related_name='lignes',
        on_delete=models.CASCADE
    )

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    quantite = models.IntegerField(default=1)

    prix_unitaire = models.FloatField(default=0)

    def montant(self):
        return self.quantite * self.prix_unitaire