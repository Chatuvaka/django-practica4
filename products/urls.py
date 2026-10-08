from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    CategoryViewSet,
    precio_final
)


router = DefaultRouter()

router.register(
    'products',
    ProductViewSet
)

router.register(
    'categories',
    CategoryViewSet
)


urlpatterns = router.urls

urlpatterns += [
    path(
        'products/<int:pk>/precio-final/',
        precio_final
    ),
]