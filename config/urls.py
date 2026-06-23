from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from avitaillement.views import stocks_page
from avitaillement.views import AvitaillementViewSet
from factures.views import FactureViewSet
from clients.views import ClientViewSet
from produits.views import ProduitViewSet
from .views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view
from .views import logout_view


router = DefaultRouter()
router.register(r'factures', FactureViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'avitaillements', AvitaillementViewSet)
from avitaillement.views import StockCuveViewSet

router.register(r'stocks',StockCuveViewSet)

urlpatterns = [
    path("login/", login_view),
    path("logout/", logout_view),
    path('', dashboard),  # ✅ PAGE D’ACCUEIL
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('factures/', include('factures.urls')),
    path('clients/', include('clients.urls')),
    path('produits/', include('produits.urls')),
    path("avitaillement/", include("avitaillement.urls")),
    path("stocks/", stocks_page),
]

# MEDIA (logo)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)