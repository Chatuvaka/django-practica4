
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API de Tienda Online",
        default_version="v1",
        description="API para administrar productos, categorías y usuarios.",
        license=openapi.License(name="Proyecto académico"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # API de productos y categorías
    path('api/', include('products.urls')),
    path('api/', include('users.urls')),

    # Autenticación JWT existente
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    # Documentación Swagger y ReDoc
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
