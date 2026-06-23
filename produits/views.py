from rest_framework import viewsets
from .models import Produit
from .serializers import ProduitSerializer
from django.shortcuts import render
from journal.models import JournalActivite
from django.contrib.auth.decorators import login_required
from config.decorators import groupe_requis
from config.permissions import EstOperateur

class ProduitViewSet(viewsets.ModelViewSet):

    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [EstOperateur]

    def perform_create(self, serializer):

        produit = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Création du produit {produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_update(self, serializer):

        produit = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Modification du produit {produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_destroy(self, instance):

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Suppression du produit {instance.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        instance.delete()

        
@login_required
@groupe_requis("Operateurs")
def produits_page(request):
    return render(request, "produits.html")