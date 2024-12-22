# 🛒 API REST de Gestión de Productos - Mi Tienda

Esta es una **API RESTful** desarrollada con **Django** y **Django Rest Framework (DRF)** para gestionar productos en una tienda en línea. El proyecto incluye funcionalidades básicas como CRUD (Crear, Leer, Actualizar, Eliminar) para productos, autenticación con tokens y documentación interactiva.

---

## 📋 **Características**

- **CRUD de productos**: Crear, consultar, actualizar y eliminar productos.
- **Autenticación**: 
  - Token de autenticación usando `DRF` y **JWT**.
- **Documentación interactiva**:
  - Swagger UI (interfaz de usuario amigable).
  - Redoc.
- **Filtrado, búsqueda y ordenación** de productos.
- **Pruebas automatizadas** con Django TestCase.
- **Gestión segura de variables sensibles** con `.env`.
- **Paginación** para mejorar el rendimiento de la API.

---

## 🚀 **Tecnologías usadas**

- **Python** 3.12
- **Django** 5.1.3
- **Django REST Framework** 3.15.2
- **drf-yasg** (Documentación interactiva)
- **Django Filter** (Filtrado de datos)
- **Simple JWT** (Autenticación JWT)
- **SQLite** (Base de datos por defecto)

---

## ⚙️ **Instalación y configuración**

Sigue los siguientes pasos para configurar y ejecutar el proyecto localmente.

1. **Clona el repositorio**

```bash
git clone https://github.com/tu-usuario/mi-tienda-api.git
cd mi-tienda-api


2. **Crea un entorno virtual**
python -m venv env
source env/bin/activate    # En Mac/Linux
env\Scripts\activate       # En Windows


3. **Instala las dependencias**
pip install --upgrade pip
pip install -r requirements.txt


4. **Crea un archivo .env**
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

4. **Realiza las migraciones**
python manage.py makemigrations
python manage.py migrate


5. **Crea un superusuario**
python manage.py createsuperuser


6. **Ejecuta el servidor**
python manage.py runserver


Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación interactiva en las siguientes rutas:

Swagger UI: http://127.0.0.1:8000/swagger/
Redoc: http://127.0.0.1:8000/redoc/


-----------------------------------------


🔑 Autenticación
La API utiliza tokens JWT y autenticación de tokens de DRF.

Obtener un token JWT
Envía una petición POST a la siguiente ruta:

bash
POST /api/token/


Cuerpo de la solicitud (JSON):
{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}

Respuesta:
{
    "access": "token_de_acceso",
    "refresh": "token_de_refresco"
}

----------------------------------

Pruebas:
python manage.py test



-----------------------------------

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Siéntete libre de abrir un issue o un pull request.

Haz un fork del repositorio.
Crea una nueva rama: git checkout -b feature/nueva-funcionalidad.
Realiza tus cambios y haz commits: git commit -m "Agrega nueva funcionalidad".
Sube los cambios: git push origin feature/nueva-funcionalidad.
Abre un pull request.

-----------------------------------

🔗 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.