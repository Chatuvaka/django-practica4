from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Manager personalizado para el modelo de Usuario donde el correo electrónico
    es el identificador único para la autenticación en lugar de username.
    """

    def create_user(self, email=None, password=None, **extra_fields):
        # Compatibilidad hacia atrás si se envía 'username' en pruebas o scripts previos
        if not email and 'username' in extra_fields:
            uname = extra_fields.pop('username')
            email = f"{uname}@example.com" if '@' not in uname else uname
        elif 'username' in extra_fields:
            extra_fields.pop('username')

        if not email:
            raise ValueError('El correo electrónico es obligatorio para crear un usuario.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que utiliza el correo electrónico como identificador único.
    Incluye campo adicional 'telefono' según los requisitos de la actividad académica.
    """

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='Correo electrónico',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nombre',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Apellido',
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Es staff / administrador',
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de registro',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name or self.email

    def __str__(self):
        return self.email

