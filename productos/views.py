from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
)
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Producto
from .serializers import ProductoSerializer
from .permissions import IsOwnerOrAdmin


# Filtro personalizado para el modelo Producto
class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(
        field_name="precio", lookup_expr="gte", label="Precio mínimo"
    )
    precio_max = django_filters.NumberFilter(
        field_name="precio", lookup_expr="lte", label="Precio máximo"
    )

    class Meta:
        model = Producto
        fields = ["precio_min", "precio_max", "nombre", "stock"]


# Vista basada en ViewSet para CRUD de Producto
class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal para gestionar productos con soporte para filtrado, búsqueda y ordenación.
    """

    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    # Configuración de filtros, búsqueda y ordenación
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductoFilter
    search_fields = ["nombre", "descripcion"]  # Campos permitidos para búsqueda
    ordering_fields = ["precio", "nombre", "stock"]  # Campos permitidos para ordenación
    ordering = ["creado_en"]  # Orden predeterminado

    def perform_create(self, serializer):
        """
        Asigna automáticamente al usuario autenticado como propietario del producto.
        """
        serializer.save(propietario=self.request.user)

    def get_queryset(self):
        """
        Sobrescribe el queryset para facilitar la depuración o personalizar consultas.
        """
        queryset = super().get_queryset()
        print(queryset.query)  # Depuración: imprime la consulta generada
        return queryset

    def get_permissions(self):
        """
        Define permisos según la acción que se está ejecutando.
        """
        if self.action == "create":
            return [IsAdminUser()]
        return super().get_permissions()


# Vista basada en clase para listar productos con filtrado
class ProductoListView(ListAPIView):
    """
    Vista para listar productos con soporte para filtrado y búsqueda.
    """

    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductoFilter

    def get_queryset(self):
        """
        Permite agregar lógica personalizada al queryset antes de aplicar filtros.
        """
        queryset = super().get_queryset()
        print(f"Queryset inicial antes de aplicar filtros: {queryset}")  # Depuración
        return queryset


# Vista basada en clase para crear productos
class ProductoCreateView(CreateAPIView):
    """
    Vista para la creación de productos. Solo usuarios autenticados pueden crear productos.
    """

    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Asigna automáticamente al usuario autenticado como propietario del producto.
        """
        serializer.save(propietario=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Sobrescribe el método POST para agregar mensajes de depuración.
        """
        print(f"Usuario en la vista: {request.user}, is_staff: {request.user.is_staff}")
        print(f"Permisos: {request.user.get_all_permissions()}")
        return super().post(request, *args, **kwargs)
