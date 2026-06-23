from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from journal.models import JournalActivite
from .models import Facture
from .serializers import FactureSerializer
from config.decorators import groupe_requis
from .generator_pdf import generate_facture_pdf
from django.shortcuts import render
from config.decorators import groupe_requis
from django.contrib.auth.decorators import login_required
from config.permissions import EstComptable
from rest_framework.permissions import AllowAny
# ===============================
# PAGE LISTE FACTURES
# ===============================
@login_required
@groupe_requis("Comptable")
def factures_page(request):
    return render(request, "factures.html")

# ===============================
# API CRUD FACTURES
# ===============================
class FactureViewSet(viewsets.ModelViewSet):

    queryset = Facture.objects.all().order_by('-id')
    serializer_class = FactureSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        facture = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="FACTURE",
            action="CREATION",
            element=facture.reference,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_update(self, serializer):

        facture = serializer.save()

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="FACTURE",
            action="MODIFICATION",
            element=facture.reference,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

    def perform_destroy(self, instance):

        JournalActivite.objects.create(
            utilisateur=self.request.user,
            module="FACTURE",
            action="SUPPRESSION",
            element=instance.reference,
            adresse_ip=self.request.META.get("REMOTE_ADDR")
        )

        instance.delete()


# ===============================
# APERÇU HTML FACTURE
# ===============================
@login_required
@groupe_requis("Comptable")
def facture_preview(request, id):
    facture = get_object_or_404(Facture, id=id)
    JournalActivite.objects.create(
    utilisateur=request.user,
    action=f"Consultation facture #{facture.id}",
    adresse_ip=request.META.get("REMOTE_ADDR")
)

    return render(request, "facture.html", {
        "facture": facture,
        "client": facture.client,
        "lignes": facture.lignes.all(),
        "logo_url": "/media/Logo.jpg"
    })


# ===============================
# PDF FACTURE
# ===============================
@login_required
@groupe_requis("Comptable")
def facture_pdf(request, id):
    facture = get_object_or_404(Facture, id=id)
    JournalActivite.objects.create(
    utilisateur=request.user,
    action=f"Téléchargement PDF facture #{facture.id}",
    adresse_ip=request.META.get("REMOTE_ADDR")
)

    pdf = generate_facture_pdf(request, facture)

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="facture_{id}.pdf"'
    )

    return response