import django_filters
from productos.models import Producto


class ProductoFilter(django_filters.FilterSet):
    """
    Filtros personalizados para el modelo Producto.
    """

    precio__gte = django_filters.NumberFilter(field_name="precio", lookup_expr="gte")
    precio__lte = django_filters.NumberFilter(field_name="precio", lookup_expr="lte")

    class Meta:
        model = Producto
        fields = ["precio__gte", "precio__lte"]
