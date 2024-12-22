from rest_framework import serializers
from .models import Producto


from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    # El propietario se representa como su nombre de usuario, y es de solo lectura
    propietario = serializers.ReadOnlyField(source="propietario.username")

    class Meta:
        model = Producto
        fields = "__all__"

    def validate_precio(self, value):
        """
        Valida que el precio sea mayor a 0.
        """
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value

    def validate_stock(self, value):
        """
        Valida que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def to_representation(self, instance):
        """
        Modifica la representación de los datos serializados.
        Convierte valores numéricos como el precio en float para mayor consistencia.
        """
        representation = super().to_representation(instance)
        if "precio" in representation:
            representation["precio"] = float(representation["precio"])
        return representation