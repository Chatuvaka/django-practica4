from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, MeView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/me/', MeView.as_view(), name='auth_me'),
    path('', include(router.urls)),
]

