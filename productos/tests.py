from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto


class ProductoAPITests(APITestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas:
        - Crear usuarios (normal y admin).
        - Crear productos de prueba.
        - Generar tokens para autenticación.
        """
        # Crear usuario normal
        self.user = User.objects.create_user(username="usuario", password="12345")
        self.user_token = Token.objects.create(user=self.user)

        # Crear usuario administrador
        self.admin = User.objects.create_superuser(
            username="admin", password="admin123"
        )
        self.admin_token = Token.objects.create(user=self.admin)

        # Crear productos de prueba
        self.producto1 = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción 1",
            precio=10.0,
            stock=5,
            propietario=self.user,
        )
        self.producto2 = Producto.objects.create(
            nombre="Producto 2",
            descripcion="Descripción 2",
            precio=20.0,
            stock=10,
            propietario=self.user,
        )
        self.producto3 = Producto.objects.create(
            nombre="Producto 3",
            descripcion="Descripción 3",
            precio=15.0,
            stock=8,
            propietario=self.user,
        )

        # Endpoint base para productos
        self.url = reverse("producto-list")

        # Cliente de pruebas
        self.client = APIClient()

    def authenticate(self, token):
        """
        Helper para autenticar solicitudes con un token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    # Pruebas de filtrado
    def test_filtrar_productos_por_precio(self):
        response = self.client.get(f"{self.url}?precio_min=15")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        productos = response.json()["results"]
        for producto in productos:
            self.assertGreaterEqual(
                float(producto["precio"]),
                15,
                msg=f"El producto {producto['nombre']} tiene precio menor a 15.",
            )

    # Pruebas de búsqueda
    def test_buscar_productos_por_nombre(self):
        response = self.client.get(f"{self.url}?search=Producto 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        productos = response.json()["results"]
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0]["nombre"], "Producto 1")

    # Pruebas de ordenación
    def test_ordenar_productos_por_precio(self):
        # Ordenar por precio ascendente
        response = self.client.get(f"{self.url}?ordering=precio")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        precios = [producto["precio"] for producto in response.json()["results"]]
        self.assertEqual(precios, sorted(precios))

        # Ordenar por precio descendente
        response = self.client.get(f"{self.url}?ordering=-precio")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        precios = [producto["precio"] for producto in response.json()["results"]]
        self.assertEqual(precios, sorted(precios, reverse=True))

    # Pruebas de errores
    def test_producto_no_encontrado(self):
        """
        Verifica que el detalle de un producto inexistente devuelva un error 404.
        """
        url = reverse("producto-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crear_producto_datos_invalidos(self):
        """
        Verifica que enviar datos inválidos al crear un producto devuelva un error 400.
        """
        self.authenticate(self.admin_token.key)
        datos_invalidos = {"nombre": "", "precio": -10, "stock": -5}
        response = self.client.post(self.url, datos_invalidos, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nombre", response.data)
        self.assertIn("precio", response.data)
        self.assertIn("stock", response.data)

    # Pruebas de autenticación y permisos
    def test_actualizar_producto_sin_autorizacion(self):
        producto = Producto.objects.create(
            nombre="Producto Prueba", precio=100, stock=10
        )
        url = reverse("producto-detail", kwargs={"pk": producto.pk})
        datos_actualizados = {"nombre": "Nuevo Nombre", "precio": 150}
        response = self.client.put(url, datos_actualizados, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acceso_no_autenticado_a_endpoint_protegido(self):
        datos = {"nombre": "Producto Test", "precio": 50, "stock": 5}
        response = self.client.post(self.url, datos, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_sin_permisos_no_puede_crear_producto(self):
        """
        Verifica que un usuario sin permisos no pueda crear un producto.
        """
        self.authenticate(self.user_token.key)
        datos = {
            "nombre": "Producto Test",
            "descripcion": "Descripción",
            "precio": 10.5,
            "stock": 50,
        }
        response = self.client.post(self.url, datos, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_usuario_admin_puede_crear_producto(self):
        """
        Verifica que un usuario administrador pueda crear un producto.
        """
        self.authenticate(self.admin_token.key)
        datos = {
            "nombre": "Producto Test",
            "descripcion": "Descripción",
            "precio": 10.5,
            "stock": 50,
        }
        response = self.client.post(self.url, datos, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nombre"], "Producto Test")
