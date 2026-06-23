from rest_framework import serializers
from .models import StockCuve, Avitaillement


class StockCuveSerializer(serializers.ModelSerializer):

    produit_nom = serializers.CharField(
        source="produit.nom",
        read_only=True
    )

    class Meta:
        model = StockCuve
        fields = "__all__"


class AvitaillementSerializer(serializers.ModelSerializer):

    produit_nom = serializers.CharField(
        source="produit.nom",
        read_only=True
    )

    unite = serializers.CharField(
        source="produit.unite",
        read_only=True
    )

    class Meta:
        model = Avitaillement
        fields = "__all__"