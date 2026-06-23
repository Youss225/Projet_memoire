from rest_framework import serializers
from .models import Facture, LigneFacture


class LigneFactureSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)

    class Meta:
        model = LigneFacture
        fields = [
            'id',
            'produit',
            'produit_nom',
            'quantite',
            'prix_unitaire'
        ]


class FactureSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    lignes = LigneFactureSerializer(many=True)

    class Meta:
        model = Facture
        fields = [
            'id',
            'reference',
            'client',
            'client_nom',
            'date',
            'date_livraison',
            'date_limite',
            'total',
            'lignes'
        ]

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')
        facture = Facture.objects.create(**validated_data)

        total = 0

        for ligne in lignes_data:
            LigneFacture.objects.create(
                facture=facture,
                **ligne
            )
            total += ligne['quantite'] * ligne['prix_unitaire']

        facture.total = total
        facture.save()

        return facture

    def update(self, instance, validated_data):
        lignes_data = validated_data.pop('lignes')

        instance.reference = validated_data.get('reference', instance.reference)
        instance.client = validated_data.get('client', instance.client)
        instance.date_livraison = validated_data.get('date_livraison')
        instance.date_limite = validated_data.get('date_limite')
        instance.save()

        instance.lignes.all().delete()

        total = 0

        for ligne in lignes_data:
            LigneFacture.objects.create(
                facture=instance,
                **ligne
            )
            total += ligne['quantite'] * ligne['prix_unitaire']

        instance.total = total
        instance.save()

        return instance