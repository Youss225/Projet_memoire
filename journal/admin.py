from django.contrib import admin
from .models import JournalActivite

@admin.register(JournalActivite)
class JournalActiviteAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "action",
        "date_action",
        "adresse_ip"
    )

    list_filter = (
        "date_action",
        "utilisateur"
    )

    search_fields = (
        "action",
        "utilisateur__username"
    )