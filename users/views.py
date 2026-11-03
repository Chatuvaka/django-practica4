from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD Administrativo de usuarios.
    Permite listar, consultar, crear, actualizar (PUT/PATCH) y eliminar usuarios.
    Protegido para que solo usuarios autorizados (administradores/staff) tengan acceso.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class MeView(APIView):
    """
    Endpoint para consultar los datos personales del usuario autenticado.
    Requiere autenticación JWT válida mediante header 'Authorization: Bearer <access_token>'.
    Retorna exclusivamente ID, Correo electrónico, Nombre, Apellido y Teléfono.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Consultar datos del usuario autenticado",
        operation_description="Devuelve exclusivamente los datos personales del usuario que posee el token JWT sin exponer contraseñas ni hashes.",
        responses={
            200: UserProfileSerializer(),
            401: "No autenticado o token inválido/expirado",
        }
    )
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

