from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    propietario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="productos", default=1
    )  # Usa un ID de usuario predeterminado

    def clean(self):
        """
        Validaciones personalizadas antes de guardar el producto.
        """
        # Validación 1: El nombre debe tener al menos 3 caracteres
        if len(self.nombre) < 3:
            raise ValidationError(
                {"nombre": "El nombre debe tener al menos 3 caracteres."}
            )

        # Validación 2: El precio debe ser mayor que 0
        if self.precio <= 0:
            raise ValidationError({"precio": "El precio debe ser mayor que 0."})

        # Validación 3: El stock no puede ser negativo
        if self.stock < 0:
            raise ValidationError({"stock": "El stock no puede ser negativo."})

    def __str__(self):
        """
        Representación en texto del modelo.
        """
        return self.nombre
