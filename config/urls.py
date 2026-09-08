from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import dashboard
from .views import login_view
from .views import logout_view

from factures.views import FactureViewSet
from clients.views import ClientViewSet
from produits.views import ProduitViewSet
from avitaillement.views import (
    AvitaillementViewSet,
    StockCuveViewSet,
    stocks_page,
)
from feedback.views import FeedbackViewSet


router = DefaultRouter()

router.register(r'factures', FactureViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'avitaillements', AvitaillementViewSet)
router.register(r'stocks', StockCuveViewSet)
router.register(r'feedback', FeedbackViewSet)


urlpatterns = [

    path("login/", login_view),
    path("logout/", logout_view),

    path("", dashboard),

    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),

    path("factures/", include("factures.urls")),
    path("clients/", include("clients.urls")),
    path("produits/", include("produits.urls")),
    path("feedback/", include("feedback.urls")),
    path("avitaillement/", include("avitaillement.urls")),
    path("stocks/", stocks_page),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)