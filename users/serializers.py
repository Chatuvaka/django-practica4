from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer completo para el CRUD administrativo de usuarios (/api/users/).
    Garantiza la protección de campos sensibles como contraseñas y hashes:
    - La contraseña es write_only y nunca se retorna en ninguna respuesta.
    - En partial_update / update, si no se envía contraseña, la actual se conserva intacta.
    - Si se envía contraseña, se almacena de forma segura mediante set_password (hash de Django).
    - Nunca se copia la contraseña de request.user ni de otra cuenta.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        style={'input_type': 'password'},
        help_text='Contraseña en texto plano para crear o actualizar el usuario. Se almacenará como hash seguro.'
    )
    nombre = serializers.CharField(
        source='first_name',
        required=False,
        allow_blank=True,
        help_text='Alias para el campo first_name'
    )
    apellido = serializers.CharField(
        source='last_name',
        required=False,
        allow_blank=True,
        help_text='Alias para el campo last_name'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'nombre',
            'apellido',
            'telefono',
            'password',
            'is_staff',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        user = self.instance
        normalized = value.lower()
        query = User.objects.filter(email__iexact=normalized)
        if user:
            query = query.exclude(pk=user.pk)
        if query.exists():
            raise serializers.ValidationError('Ya existe un usuario registrado con este correo electrónico.')
        return normalized

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Corrección de seguridad del manual:
        # 1. Extraemos password solo si fue enviado explícitamente.
        password = validated_data.pop('password', None)

        # 2. Actualizamos el resto de los campos regulares (nombre, email, telefono, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 3. Solo si se proporcionó una contraseña nueva y no vacía, se actualiza mediante hash.
        # Si no se envió 'password', la contraseña existente del usuario permanece intacta.
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Salvaguarda adicional: jamás exponer campos de contraseña
        ret.pop('password', None)
        return ret


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer exclusivo para el endpoint de datos personales (/api/auth/me/).
    Devuelve estrictamente los campos requeridos sin hashes ni contraseñas.
    """

    nombre = serializers.CharField(source='first_name', read_only=True)
    apellido = serializers.CharField(source='last_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'nombre',
            'apellido',
            'telefono',
        ]
        read_only_fields = fields

