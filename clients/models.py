from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    ncc = models.CharField(max_length=50, blank=True)