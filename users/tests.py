from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAuthenticationAndSecurityTestCase(TestCase):
    """
    Pruebas automatizadas para:
    - Creación de usuarios con contraseñas seguras mediante hash.
    - Autenticación con correo electrónico y contraseña.
    - Obtención de tokens JWT (access y refresh).
    - Consulta de datos personales en /api/auth/me/ con token JWT.
    - Rechazo de solicitudes sin token (401 Unauthorized).
    - CRUD completo de usuarios en /api/users/.
    - Control de permisos: acceso solo a administradores.
    - Corrección de seguridad: actualizar sin enviar contraseña no altera la contraseña.
    - Cambio exitoso de contraseña mediante hash seguro.
    - Garantía de no exposición de contraseñas o hashes en ninguna respuesta.
    """

    def setUp(self):
        self.client = APIClient()

        # Usuario administrador para gestionar el CRUD
        self.admin_user = User.objects.create_superuser(
            email='admin@tienda.com',
            password='AdminPassword123!',
            first_name='Admin',
            last_name='Sistema',
            telefono='5551234567'
        )

        # Usuario estándar para pruebas de autenticación y perfil
        self.regular_user = User.objects.create_user(
            email='cliente@tienda.com',
            password='ClientePassword123!',
            first_name='Carlos',
            last_name='Gomez',
            telefono='5559876543'
        )

    def test_crear_usuario_con_hash_seguro(self):
        """Verifica que el usuario se crea con contraseña protegida mediante hash."""
        user = User.objects.create_user(
            email='nuevo@tienda.com',
            password='PasswordSegura2026!',
            first_name='Laura',
            last_name='Mendoza',
            telefono='5554443322'
        )
        self.assertEqual(user.email, 'nuevo@tienda.com')
        self.assertNotEqual(user.password, 'PasswordSegura2026!')
        self.assertTrue(user.check_password('PasswordSegura2026!'))
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))

    def test_autenticacion_jwt_con_correo(self):
        """Verifica login con correo y contraseña en /api/token/ devolviendo JWT."""
        response = self.client.post(
            '/api/token/',
            {
                'email': 'cliente@tienda.com',
                'password': 'ClientePassword123!'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_autenticacion_jwt_credenciales_invalidas(self):
        """Verifica que rechace credenciales incorrectas."""
        response = self.client.post(
            '/api/token/',
            {
                'email': 'cliente@tienda.com',
                'password': 'PasswordIncorrecta'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_jwt(self):
        """Verifica la renovación de token en /api/token/refresh/."""
        token_resp = self.client.post(
            '/api/token/',
            {
                'email': 'cliente@tienda.com',
                'password': 'ClientePassword123!'
            },
            format='json'
        )
        refresh_token = token_resp.data['refresh']

        refresh_resp = self.client.post(
            '/api/token/refresh/',
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_resp.data)

    def test_consultar_datos_personales_con_token(self):
        """Verifica el endpoint /api/auth/me/ con autenticación JWT."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.regular_user.id)
        self.assertEqual(response.data['email'], 'cliente@tienda.com')
        self.assertEqual(response.data['first_name'], 'Carlos')
        self.assertEqual(response.data['last_name'], 'Gomez')
        self.assertEqual(response.data['telefono'], '5559876543')

        # Verificar que no expone información sensible
        self.assertNotIn('password', response.data)
        self.assertNotIn('is_superuser', response.data)
        self.assertNotIn('user_permissions', response.data)

    def test_rechazar_solicitud_sin_token(self):
        """Verifica rechazo con código 401 sin token de autenticación."""
        # Cliente sin autenticar
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # CRUD sin autenticar también rechazado
        crud_response = self.client.get('/api/users/')
        self.assertEqual(crud_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crud_usuarios_permiso_administrativo(self):
        """Verifica que usuarios no administradores no puedan acceder al CRUD."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crud_usuarios_operaciones_admin(self):
        """Verifica operaciones completas de CRUD por un usuario administrador."""
        self.client.force_authenticate(user=self.admin_user)

        # 1. Listar usuarios
        list_resp = self.client.get('/api/users/')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_resp.data), 2)

        # 2. Crear usuario via POST
        create_resp = self.client.post(
            '/api/users/',
            {
                'email': 'maria@tienda.com',
                'password': 'MariaPassword2026!',
                'first_name': 'Maria',
                'last_name': 'Lopez',
                'telefono': '5551112233'
            },
            format='json'
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        new_id = create_resp.data['id']
        self.assertNotIn('password', create_resp.data)

        # 3. Consultar detalle via GET
        detail_resp = self.client.get(f'/api/users/{new_id}/')
        self.assertEqual(detail_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_resp.data['email'], 'maria@tienda.com')
        self.assertNotIn('password', detail_resp.data)

        # 4. Actualizar via PUT
        put_resp = self.client.put(
            f'/api/users/{new_id}/',
            {
                'email': 'maria_actualizada@tienda.com',
                'first_name': 'Maria Teresa',
                'last_name': 'Lopez',
                'telefono': '5559998877'
            },
            format='json'
        )
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(put_resp.data['first_name'], 'Maria Teresa')

        # 5. Eliminar via DELETE
        del_resp = self.client.delete(f'/api/users/{new_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=new_id).exists())

    def test_actualizar_usuario_sin_password_conserva_password_anterior(self):
        """
        Corrección de seguridad clave:
        Al actualizar mediante PATCH o PUT sin enviar 'password',
        la contraseña anterior DEBE conservarse intacta y seguir funcionando.
        """
        self.client.force_authenticate(user=self.admin_user)
        original_hash = self.regular_user.password

        # Actualizamos solo nombre y teléfono
        response = self.client.patch(
            f'/api/users/{self.regular_user.id}/',
            {
                'first_name': 'Carlos Alberto',
                'telefono': '5550001122'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.first_name, 'Carlos Alberto')
        self.assertEqual(self.regular_user.telefono, '5550001122')

        # La contraseña no debe haber cambiado
        self.assertEqual(self.regular_user.password, original_hash)
        self.assertTrue(self.regular_user.check_password('ClientePassword123!'))

        # Verificación directa: el login sigue funcionando con la contraseña anterior
        auth_client = APIClient()
        login_resp = auth_client.post(
            '/api/token/',
            {
                'email': 'cliente@tienda.com',
                'password': 'ClientePassword123!'
            },
            format='json'
        )
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

    def test_actualizar_password_con_hash_seguro(self):
        """
        Verifica que enviar una nueva contraseña en PATCH o PUT la almacena con hash seguro,
        la contraseña anterior deja de funcionar y la nueva funciona.
        """
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.patch(
            f'/api/users/{self.regular_user.id}/',
            {
                'password': 'NuevaPassword2026!'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('NuevaPassword2026!'))
        self.assertFalse(self.regular_user.check_password('ClientePassword123!'))

        # Probar autenticación con la nueva contraseña
        auth_client = APIClient()
        new_login = auth_client.post(
            '/api/token/',
            {
                'email': 'cliente@tienda.com',
                'password': 'NuevaPassword2026!'
            },
            format='json'
        )
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)

    def test_no_se_copia_password_de_usuario_autenticado(self):
        """
        Verifica que la contraseña del usuario autenticado (admin) NUNCA se copia
        a la cuenta del usuario editado.
        """
        self.client.force_authenticate(user=self.admin_user)
        admin_hash = self.admin_user.password

        # Editamos al usuario regular
        self.client.patch(
            f'/api/users/{self.regular_user.id}/',
            {'first_name': 'NuevoNombre'},
            format='json'
        )

        self.regular_user.refresh_from_db()
        self.assertNotEqual(self.regular_user.password, admin_hash)
        self.assertFalse(self.regular_user.check_password('AdminPassword123!'))

    def test_no_se_expone_hash_o_password_en_ningun_endpoint(self):
        """
        Garantiza que la contraseña o su hash jamás aparezca en respuestas JSON
        del CRUD ni del endpoint /api/auth/me/.
        """
        self.client.force_authenticate(user=self.admin_user)

        # 1. En listado
        list_resp = self.client.get('/api/users/')
        for item in list_resp.data:
            self.assertNotIn('password', item)
            for key, val in item.items():
                self.assertNotIn('pbkdf2', str(val))

        # 2. En detalle
        detail_resp = self.client.get(f'/api/users/{self.regular_user.id}/')
        self.assertNotIn('password', detail_resp.data)
        for key, val in detail_resp.data.items():
            self.assertNotIn('pbkdf2', str(val))

        # 3. En /api/auth/me/
        self.client.force_authenticate(user=self.regular_user)
        me_resp = self.client.get('/api/auth/me/')
        self.assertNotIn('password', me_resp.data)
        for key, val in me_resp.data.items():
            self.assertNotIn('pbkdf2', str(val))

