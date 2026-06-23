from decimal import Decimal

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from journal.models import JournalActivite
from .models import StockCuve, Avitaillement
from .serializers import ( StockCuveSerializer,AvitaillementSerializer)
from config.decorators import groupe_requis
from django.contrib.auth.decorators import login_required
from config.permissions import EstOperateur

# ==========================
# PAGE AVITAILLEMENTS
# ==========================
@login_required
@groupe_requis("Operateurs")
def page_avitaillement(request):
    return render(request, "avitaillement.html")

# ==========================
# PAGE STOCKS
# ==========================

@login_required
@groupe_requis("Operateurs")
def stocks_page(request):
    return render(request, "stocks.html")


# ==========================
# STOCKS
# ==========================

class StockCuveViewSet(viewsets.ModelViewSet):
    queryset = StockCuve.objects.all()
    serializer_class = StockCuveSerializer
    permissions_classes = [EstOperateur]
    @action(
        detail=False,
        methods=["get"]
    )
    def resume(self, request):

        total_stock = sum(
            stock.stock_actuel
            for stock in StockCuve.objects.all()
        )

        nb_alertes = StockCuve.objects.filter(
            stock_actuel__lte=Decimal("1000")
        ).count()

        return Response({
            "total_stock": total_stock,
            "nb_alertes": nb_alertes
        })

    def perform_create(self, serializer):

        stock = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Création stock {stock.produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_update(self, serializer):

        stock = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Modification stock {stock.produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_destroy(self, instance):

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Suppression stock {instance.produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        instance.delete()


# ==========================
# AVITAILLEMENTS
# ==========================


from django.shortcuts import render
@login_required
@groupe_requis("Operateurs")
def page_avitaillement(request):
    return render(request, "avitaillement.html")

class AvitaillementViewSet(viewsets.ModelViewSet):

    queryset = Avitaillement.objects.all().order_by("-id")
    serializer_class = AvitaillementSerializer
    permission_classes =[EstOperateur]

    def perform_create(self, serializer):

        avitaillement = serializer.save()

        stock = StockCuve.objects.get(
            produit=avitaillement.produit
        )

        stock.stock_actuel -= avitaillement.quantite
        stock.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Avitaillement de {avitaillement.quantite} L de {avitaillement.produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )
        
    def perform_update(self, serializer):

        ancien = self.get_object()

        ancienne_quantite = ancien.quantite

        avitaillement = serializer.save()

        difference = (avitaillement.quantite -ancienne_quantite)
        
        stock = StockCuve.objects.get(
            produit=avitaillement.produit
        )

        JournalActivite.objects.create(
        utilisateur=self.request.user,
        action=f"Modification avitaillement #{avitaillement.id}",
        adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        stock.stock_actuel -= difference
        stock.save()

    def perform_destroy(self, instance):

        stock = StockCuve.objects.get(
            produit=instance.produit
        )

        stock.stock_actuel += instance.quantite
        stock.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            action=f"Suppression avitaillement {instance.quantite} L de {instance.produit.nom}",
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        instance.delete()