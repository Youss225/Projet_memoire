from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer
from django.shortcuts import render
from journal.models import JournalActivite
from config.decorators import groupe_requis
from django.contrib.auth.decorators import login_required
from config.permissions import EstComptable

@login_required
@groupe_requis("Comptable")
def page_clients(request):
    return render(request, 'clients.html')

class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):

        client = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="CLIENT",
            action="CREATION",
            element=client.nom,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_update(self, serializer):

        client = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="CLIENT",
            action="MODIFICATION",
            element=client.nom,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_destroy(self, instance):

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="CLIENT",
            action="SUPPRESSION",
            element=instance.nom,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        instance.delete()