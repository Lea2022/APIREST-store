from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Permiso personalizado:
    - Cualquier usuario puede leer datos (SAFE_METHODS).
    - Solo el propietario del recurso o un admin pueden realizar modificaciones.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir acceso de lectura a cualquier usuario
        if request.method in SAFE_METHODS:
            return True

        # Permitir escritura/eliminación solo al propietario o admin
        return request.user == obj.propietario or request.user.is_staff
