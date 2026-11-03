# GUÍA DE EVIDENCIAS — API REST TIENDA ONLINE

Esta guía paso a paso te explica cómo tomar cada una de las capturas de pantalla requeridas para el reporte final de tu actividad académica. Sigue el orden establecido y copia los textos sugeridos debajo de cada imagen en tu documento PDF.

---

## 📋 Resumen Rápido de Preparación

Antes de iniciar con las capturas, abre una terminal (PowerShell o CMD) en la carpeta del proyecto y ejecuta el servidor de Django:

```bash
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

Asegúrate de tener abiertos:
1. Tu navegador web (Chrome, Edge o Firefox).
2. Un cliente de APIs: Postman, Insomnia, Thunder Client en VS Code o la propia interfaz de Swagger en el navegador.

---

## 📸 Catálogo Ordenado de Evidencias

---

### Evidencia 1: Proyecto ejecutándose

- **Nombre sugerido:** `evidencia_01_proyecto_ejecutandose.png`
- **Requisito que demuestra:** Servidor de desarrollo de Django iniciado correctamente sin errores de configuración ni migraciones pendientes.
- **Programa a abrir:** Terminal (PowerShell / Símbolo del sistema).
- **URL o endpoint:** `http://127.0.0.1:8000/`
- **Procedimiento:**
  1. En la terminal del proyecto, escribe: `python manage.py runserver` y presiona Enter.
  2. Espera a que aparezca el mensaje de inicio del servidor indicando la versión de Django y la URL `http://127.0.0.1:8000/`.
  3. Toma la captura de la ventana de la terminal.
- **Qué debe verse claramente:**
  - `Django version 5.2.17 using settings 'tienda_online.settings'`
  - `Starting development server at http://127.0.0.1:8000/`
  - `Quit the server with CTRL-BREAK.`
- **Texto para colocar debajo de la imagen:** *Figura 1. Servidor de desarrollo de Django 5.2 ejecutándose localmente en el puerto 8000.*
- **Sección del PDF:** Introducción / Entorno de desarrollo.

---

### Evidencia 2: Swagger con endpoints documentados

- **Nombre sugerido:** `evidencia_02_swagger_ui.png`
- **Requisito que demuestra:** Configuración de `drf-yasg`, Swagger UI interactivo y documentación de los endpoints de la API (productos, categorías, usuarios y autenticación JWT).
- **Programa a abrir:** Navegador Web.
- **URL o endpoint:** `http://127.0.0.1:8000/swagger/`
- **Procedimiento:**
  1. Ingresa a `http://127.0.0.1:8000/swagger/` en tu navegador.
  2. Observa el título "API de Tienda Online", la versión "v1" y el botón verde "Authorize" en la esquina superior derecha.
  3. Expande los bloques de endpoints (`auth`, `categories`, `products`, `users`, `token`).
  4. Toma la captura de la pantalla completa del navegador.
- **Qué debe verse claramente:**
  - Título: `API de Tienda Online v1`.
  - Botón: `Authorize` (indicando soporte para `Bearer <access_token>`).
  - Lista de rutas: `/api/users/`, `/api/auth/me/`, `/api/token/`, `/api/products/`, etc.
- **Texto para colocar debajo de la imagen:** *Figura 2. Documentación interactiva de la API REST mediante Swagger UI (drf-yasg).*
- **Sección del PDF:** Documentación de la API / Swagger.

---

### Evidencia 3: Modelo de usuario y campo teléfono en Django Admin

- **Nombre sugerido:** `evidencia_03_admin_usuario_telefono.png`
- **Requisito que demuestra:** Integración del modelo de usuario personalizado (`users.User`), autenticación por correo electrónico y presencia del campo `telefono`.
- **Programa a abrir:** Navegador Web.
- **URL o endpoint:** `http://127.0.0.1:8000/admin/users/user/` (o formulario de edición de un usuario en `/admin/users/user/1/change/`).
- **Procedimiento:**
  1. Entra a `http://127.0.0.1:8000/admin/`.
  2. Inicia sesión con las credenciales del superusuario (`chatuvaka700@gmail.com`).
  3. Haz clic en "Usuarios" en la sección "Gestión de Usuarios".
  4. Haz clic sobre el usuario para ver su formulario detallado.
  5. Asegúrate de mostrar la sección "Información Personal" con los campos: Nombre, Apellido y **Teléfono**.
  6. Toma la captura.
- **Qué debe verse claramente:**
  - El panel Django Admin con la sección de Usuarios.
  - El campo "Correo electrónico" como identificador.
  - El campo editable "Teléfono".
- **Texto para colocar debajo de la imagen:** *Figura 3. Panel de administración de Django mostrando el modelo de usuario personalizado con el campo de teléfono integrado.*
- **Sección del PDF:** Modelo de datos / Modelo de usuario personalizado.

---

### Evidencia 4: CRUD de usuarios (Listado o creación en API)

- **Nombre sugerido:** `evidencia_04_crud_usuarios_list.png`
- **Requisito que demuestra:** Funcionamiento del endpoint administrativo `GET /api/users/` o `POST /api/users/` protegido para administradores.
- **Programa a abrir:** Postman / Insomnia / Swagger UI.
- **URL o endpoint:** `http://127.0.0.1:8000/api/users/`
- **Procedimiento:**
  1. En Postman, crea una petición `GET` a `http://127.0.0.1:8000/api/users/`.
  2. En la pestaña **Headers**, añade: `Authorization: Bearer <TOKEN_DE_ADMINISTRADOR>` (obtenido en el login).
  3. Presiona **Send**.
  4. Observa el estado `200 OK` y el array JSON con los usuarios registrados (con `id`, `email`, `first_name`, `last_name`, `telefono`, etc.).
  5. Toma la captura.
- **Qué debe verse claramente:**
  - Método `GET` y URL `http://127.0.0.1:8000/api/users/`.
  - Código de estado `200 OK`.
  - Cuerpo de respuesta JSON con la lista de usuarios.
  - Ausencia absoluta del campo de contraseña o hash en la respuesta.
- **Texto para colocar debajo de la imagen:** *Figura 4. Consulta del listado administrativo de usuarios mediante GET /api/users/ con permisos de staff.*
- **Sección del PDF:** Endpoints de la API / CRUD de usuarios.

---

### Evidencia 5: Login mediante correo y contraseña

- **Nombre sugerido:** `evidencia_05_login_email_password.png`
- **Requisito que demuestra:** Autenticación por correo electrónico en lugar de nombre de usuario en el endpoint `/api/token/`.
- **Programa a abrir:** Postman / Insomnia / Swagger UI.
- **URL o endpoint:** `POST http://127.0.0.1:8000/api/token/`
- **Procedimiento:**
  1. Configura una petición `POST` hacia `http://127.0.0.1:8000/api/token/`.
  2. En la pestaña **Body** selecciona **raw** y formato **JSON**.
  3. Ingresa el JSON con el correo y contraseña:
     ```json
     {
       "email": "chatuvaka700@gmail.com",
       "password": "<tu_contraseña>"
     }
     ```
  4. Toma la captura mostrando los datos ingresados antes de enviar o justo antes de la respuesta.
- **Qué debe verse claramente:**
  - Método `POST`, URL `/api/token/`.
  - Body JSON con `"email"` y `"password"`.
- **Texto para colocar debajo de la imagen:** *Figura 5. Solicitud de inicio de sesión utilizando correo electrónico y contraseña como credenciales de acceso.*
- **Sección del PDF:** Seguridad y Autenticación JWT.

---

### Evidencia 6: Token JWT obtenido (Access y Refresh)

- **Nombre sugerido:** `evidencia_06_tokens_jwt_obtenidos.png`
- **Requisito que demuestra:** Emisión exitosa de tokens JWT (`access` y `refresh`) mediante Django REST Framework SimpleJWT.
- **Programa a abrir:** Postman / Insomnia / Swagger UI.
- **URL o endpoint:** `POST http://127.0.0.1:8000/api/token/`
- **Procedimiento:**
  1. Con la petición del punto anterior enviada, visualiza la respuesta devuelta por el servidor.
  2. Observa el estado `200 OK` y el JSON con las claves `refresh` y `access`.
  3. Toma la captura donde se aprecie claramente la respuesta completa.
- **Qué debe verse claramente:**
  - Código `200 OK`.
  - Campo `"refresh": "eyJhbGciOi..."`.
  - Campo `"access": "eyJhbGciOi..."`.
- **Texto para colocar debajo de la imagen:** *Figura 6. Respuesta del endpoint /api/token/ entregando los tokens JWT de acceso y refresco.*
- **Sección del PDF:** Seguridad y Autenticación JWT.

---

### Evidencia 7: Endpoint `/api/auth/me/` funcionando con token

- **Nombre sugerido:** `evidencia_07_auth_me_exitoso.png`
- **Requisito que demuestra:** Consulta de datos personales del usuario en sesión (`id`, `email`, `nombre`, `apellido`, `telefono`) protegido con JWT.
- **Programa a abrir:** Postman / Insomnia / Swagger UI.
- **URL o endpoint:** `GET http://127.0.0.1:8000/api/auth/me/`
- **Procedimiento:**
  1. Configura una petición `GET` hacia `http://127.0.0.1:8000/api/auth/me/`.
  2. En la pestaña **Headers** añade:
     - Key: `Authorization`
     - Value: `Bearer <tu_access_token>`
  3. Presiona **Send**.
  4. Observa el código `200 OK` y el JSON con los datos personales exclusivamente.
  5. Toma la captura.
- **Qué debe verse claramente:**
  - Método `GET` a `/api/auth/me/`.
  - Header `Authorization: Bearer ...`.
  - Código `200 OK`.
  - Respuesta con `id`, `email`, `nombre`, `apellido` y `telefono`.
  - Ningún dato sensible (sin password ni hashes).
- **Texto para colocar debajo de la imagen:** *Figura 7. Consulta exitosa de los datos del usuario autenticado mediante el endpoint /api/auth/me/.*
- **Sección del PDF:** Endpoints de Usuario / Datos Personales.

---

### Evidencia 8: Solicitud rechazada sin token (401 Unauthorized)

- **Nombre sugerido:** `evidencia_08_solicitud_rechazada_401.png`
- **Requisito que demuestra:** Protección efectiva de los endpoints privados frente a solicitudes sin credenciales JWT.
- **Programa a abrir:** Postman / Insomnia.
- **URL o endpoint:** `GET http://127.0.0.1:8000/api/auth/me/`
- **Procedimiento:**
  1. En Postman, abre la petición a `GET http://127.0.0.1:8000/api/auth/me/`.
  2. Desmarca o elimina el header `Authorization`.
  3. Presiona **Send**.
  4. Observa la respuesta con código `401 Unauthorized`.
  5. Toma la captura.
- **Qué debe verse claramente:**
  - Código de respuesta `401 Unauthorized`.
  - Mensaje: `{"detail": "Authentication credentials were not provided."}`.
- **Texto para colocar debajo de la imagen:** *Figura 8. Rechazo con código HTTP 401 Unauthorized al intentar acceder a /api/auth/me/ sin token JWT.*
- **Sección del PDF:** Pruebas de Seguridad / Control de Acceso.

---

### Evidencia 9: Actualización de usuario sin enviar contraseña (PATCH)

- **Nombre sugerido:** `evidencia_09_patch_usuario_sin_password.png`
- **Requisito que demuestra:** Corrección de seguridad en `partial_update`: actualizar datos del usuario (nombre, teléfono) omitiendo la contraseña no modifica ni corrompe la contraseña existente.
- **Programa a abrir:** Postman / Insomnia.
- **URL o endpoint:** `PATCH http://127.0.0.1:8000/api/users/<id>/`
- **Procedimiento:**
  1. Con token de administrador en el header `Authorization: Bearer <token_admin>`.
  2. Crea una petición `PATCH` a `http://127.0.0.1:8000/api/users/<id>/`.
  3. En el Body JSON envía únicamente los datos a cambiar, por ejemplo:
     ```json
     {
       "first_name": "Nombre Actualizado",
       "telefono": "5559990011"
     }
     ```
  4. Presiona **Send**.
  5. Observa el estado `200 OK` con los datos actualizados y sin campo de contraseña.
  6. Toma la captura.
- **Qué debe verse claramente:**
  - Método `PATCH` a `/api/users/<id>/`.
  - Body sin campo `"password"`.
  - Estado `200 OK` reflejando los campos actualizados.
- **Texto para colocar debajo de la imagen:** *Figura 9. Actualización parcial de usuario sin enviar contraseña (PATCH), manteniendo la contraseña original.*
- **Sección del PDF:** Correcciones de Seguridad / Manejo Seguro de Contraseñas.

---

### Evidencia 10: Verificación de que la contraseña anterior sigue funcionando

- **Nombre sugerido:** `evidencia_10_login_password_conservada.png`
- **Requisito que demuestra:** Comprobación práctica de que la contraseña del usuario actualizado en el punto anterior no fue borrada, sobreescrita ni alterada.
- **Programa a abrir:** Postman / Insomnia.
- **URL o endpoint:** `POST http://127.0.0.1:8000/api/token/`
- **Procedimiento:**
  1. Haz un `POST` a `http://127.0.0.1:8000/api/token/` usando el correo del usuario editado y **su contraseña original**.
  2. Presiona **Send**.
  3. Observa que el servidor responde con `200 OK` y genera un nuevo par de tokens JWT.
  4. Toma la captura.
- **Qué debe verse claramente:**
  - Método `POST` a `/api/token/`.
  - Correo del usuario modificado y su contraseña previa.
  - Código de estado `200 OK` con nuevo token JWT generado exitosamente.
- **Texto para colocar debajo de la imagen:** *Figura 10. Autenticación exitosa confirmando que la contraseña previa sigue vigente tras la actualización parcial.*
- **Sección del PDF:** Correcciones de Seguridad / Verificación de Integridad.

---

### Evidencia 11: Pruebas automatizadas exitosas (20 de 20 tests)

- **Nombre sugerido:** `evidencia_11_tests_exitosos.png`
- **Requisito que demuestra:** Verificación integral y automatizada del catálogo de productos y de la seguridad de usuarios con 100% de pruebas aprobadas.
- **Programa a abrir:** Terminal (PowerShell / Símbolo del sistema).
- **URL o endpoint:** `python manage.py test`
- **Procedimiento:**
  1. En la terminal del proyecto, ejecuta:
     ```bash
     python manage.py test
     ```
  2. Espera a que se ejecute la suite de pruebas completa.
  3. Observa la salida final con los 20 puntos, el resultado `OK` y el total de 20 pruebas ejecutadas.
  4. Toma la captura de la terminal completa.
- **Qué debe verse claramente:**
  - Comando: `python manage.py test`.
  - `Creating test database for alias 'default'...`
  - Veinte puntos de éxito (`....................`).
  - `Ran 20 tests in ...s`.
  - `OK`.
  - `System check identified no issues (0 silenced).`
- **Texto para colocar debajo de la imagen:** *Figura 11. Ejecución de la suite completa de pruebas unitarias y de integración obteniendo un resultado 100% satisfactorio (OK).*
- **Sección del PDF:** Pruebas y Validación Automatizada.

---

### Evidencia 12: Repositorio GitHub con el proyecto preparado

- **Nombre sugerido:** `evidencia_12_repositorio_github.png`
- **Requisito que demuestra:** Proyecto estructurado y preparado para control de versiones en GitHub, con `.gitignore`, `requirements.txt` y `README.md` configurados.
- **Programa a abrir:** Navegador Web (página de tu repositorio en GitHub) o Terminal (`git status`).
- **Procedimiento:**
  1. Una vez que hayas hecho `git add .`, `git commit -m "Implementacion completa API REST"` y `git push` a tu repositorio de GitHub:
  2. Abre tu repositorio en GitHub en el navegador.
  3. Asegúrate de que se visualicen los archivos `README.md`, `requirements.txt`, `.gitignore`, las carpetas `tienda_online`, `products`, `users`, y que **NO** aparezcan `venv` ni `.env`.
  4. Toma la captura de la página del repositorio.
- **Qué debe verse claramente:**
  - Cabecera del repositorio con tu usuario de GitHub.
  - Estructura limpia de archivos: `products/`, `tienda_online/`, `users/`, `.gitignore`, `requirements.txt`, `README.md`.
  - Ausencia de carpetas sensibles o temporales.
- **Texto para colocar debajo de la imagen:** *Figura 12. Estructura del repositorio en GitHub con código fuente, dependencias y documentación.*
- **Sección del PDF:** Entregables / Repositorio de Código Fuente.

