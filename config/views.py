from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from journal.models import JournalActivite
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from config.decorators import groupe_requis

@login_required
def dashboard(request):

    activites = []

    if request.user.is_superuser:
        activites = JournalActivite.objects.all()[:10]

    return render(
        request,
        "dashboard.html",
        {
            "activites": activites
        }
    )

def login_view(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            JournalActivite.objects.create(
                utilisateur=user,
                action="Connexion à la plateforme",
                adresse_ip=request.META.get("REMOTE_ADDR")
            )

            return redirect("/")

        return render(
            request,
            "login.html",
            {
                "error": "Nom d'utilisateur ou mot de passe incorrect"
            }
        )

    return render(request, "login.html")


def logout_view(request):
    if request.user.is_authenticated:

        JournalActivite.objects.create(
        utilisateur=request.user,
        action="Déconnexion",
        adresse_ip=request.META.get("REMOTE_ADDR")
    )
    if request.user.is_authenticated:
        ip = request.META.get("REMOTE_ADDR")
        JournalActivite.objects.create(
            utilisateur=request.user,
            action="Déconnexion de la plateforme",
            adresse_ip=ip
        )
    logout(request)
    return redirect("/login/")