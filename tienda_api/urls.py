from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Configuración de rutas
urlpatterns = [
    # Administración de Django
    path("admin/", admin.site.urls),

    # Rutas de la API
    path("api/", include("productos.urls")),

    # Autenticación con Tokens (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentación de la API con drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # Esquema de la API
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),  # Swagger
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # Redoc
]