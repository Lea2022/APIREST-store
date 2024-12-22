from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import ProductoViewSet, ProductoListView, ProductoCreateView

router = DefaultRouter()
router.register(r"productos", ProductoViewSet, basename="producto")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += [
    path("api/token/", obtain_auth_token, name="obtain_token"),
    path("productos/", ProductoListView.as_view(), name="producto-list"),
    path("productos/", ProductoCreateView.as_view(), name="producto-create"),
]
