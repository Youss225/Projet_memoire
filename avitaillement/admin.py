from django.contrib import admin
from .models import StockCuve, Avitaillement


# ==========================
# STOCK CUVE
# ==========================

@admin.register(StockCuve)
class StockCuveAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "produit",
        "stock_actuel",
        "capacite_totale",
        "seuil_alerte",
    )


# ==========================
# AVITAILLEMENT
# ==========================

@admin.register(Avitaillement)
class AvitaillementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "date_operation",
        "nom_navire",
        "type_transport",
        "produit",
        "quantite",
        "destination",
        "consignataire",
    )

    list_filter = (
        "type_transport",
        "produit",
    )

    search_fields = (
        "nom_navire",
        "destination",
        "consignataire",
    )