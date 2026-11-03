# API REST Tienda Online con Django

API REST para la administración de productos, categorías y usuarios de una tienda online, desarrollada con Django, Django REST Framework, autenticación mediante JSON Web Tokens (JWT), base de datos relacional MySQL y documentación interactiva mediante Swagger (OpenAPI) y ReDoc.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.11+
- **Framework Web:** Django 5.2.17
- **API Toolkit:** Django REST Framework (DRF) 3.18.1
- **Autenticación:** Django REST Framework SimpleJWT 5.5.1
- **Documentación Swagger:** drf-yasg 1.21.18
- **Base de Datos:** MySQL (conector `mysqlclient`)

---

## ⚙️ Configuración y Requisitos Previos

### 1. Base de Datos MySQL

Asegúrate de contar con MySQL en ejecución y crear la base de datos:

```sql
CREATE DATABASE django_api CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

Las credenciales por defecto se configuran en `tienda_online/settings.py`:
- **Nombre BD:** `django_api`
- **Usuario:** `root`
- **Host:** `localhost`
- **Puerto:** `3306`

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio y acceder a la carpeta

```bash
git clone <URL_DEL_REPOSITORIO>
cd django-project
```

### 2. Crear y activar entorno virtual

```bash
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional si ya existe)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará accesible en: `http://127.0.0.1:8000/`

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye pruebas completas para el catálogo de productos y el sistema seguro de usuarios:

```bash
python manage.py test
```

---

## 📌 Endpoints Principales de la API

### 📄 Documentación Interactiva
- `GET /swagger/` — Interfaz interactiva de Swagger UI (compatible con `Bearer <token>`).
- `GET /redoc/` — Documentación detallada en formato ReDoc.

### 🔐 Autenticación JWT
- `POST /api/token/` — Inicio de sesión con `email` y `password` para obtener `access` y `refresh` token.
- `POST /api/token/refresh/` — Renovación del token de acceso con `refresh` token.
- `GET /api/auth/me/` — Datos personales del usuario autenticado (`id`, `email`, `nombre`, `apellido`, `telefono`). Requiere header `Authorization: Bearer <access_token>`.

### 👥 Administración de Usuarios (CRUD Administrativo - Solo Staff/Admin)
- `GET /api/users/` — Listar todos los usuarios.
- `POST /api/users/` — Registrar un nuevo usuario con contraseña cifrada con hash seguro.
- `GET /api/users/<id>/` — Consultar detalle de un usuario específico.
- `PUT /api/users/<id>/` — Actualización total de usuario.
- `PATCH /api/users/<id>/` — Actualización parcial de usuario (sin modificar la contraseña si este campo se omite).
- `DELETE /api/users/<id>/` — Eliminar un usuario.

### 📦 Productos y Categorías (Requiere Autenticación)
- `GET, POST /api/categories/` — Listar y crear categorías.
- `GET, PUT, PATCH, DELETE /api/categories/<id>/` — Administrar una categoría.
- `GET, POST /api/products/` — Listar y registrar productos.
- `GET, PUT, PATCH, DELETE /api/products/<id>/` — Administrar un producto.
- `GET /api/products/<id>/precio-final/` — Calcular precio final con descuento según categoría.

