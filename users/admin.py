from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración de administración para el modelo User personalizado en Django Admin.
    """

    ordering = ['email']
    list_display = [
        'email',
        'first_name',
        'last_name',
        'telefono',
        'is_staff',
        'is_active',
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'telefono']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'telefono')
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'telefono',
                'is_staff',
                'is_active',
            ),
        }),
    )

