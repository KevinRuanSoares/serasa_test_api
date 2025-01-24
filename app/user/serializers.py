"""
Serializers for the user API View.
"""
from datetime import datetime
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from utils.file_converters import convert_base64_to_file
from user.models import Role


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    roles = serializers.SerializerMethodField()
    role_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    profile_photo_base64 = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'name',
            'cpf',
            'phone_number',
            'profile_photo',
            'profile_photo_base64',
            'roles',
            'role_names'
        ]
        read_only_fields = ('id', 'profile_photo',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'required': False}}

    def get_roles(self, obj):
        return [role.name for role in obj.roles.all()]

    def create(self, validated_data):
        role_names = validated_data.pop('role_names', [])
        profile_photo_base64 = validated_data.pop('profile_photo_base64', None)
        password = validated_data.get('password')
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})
        user = get_user_model().objects.create_user(**validated_data)
        roles = Role.objects.filter(name__in=role_names)
        user.roles.set(roles)
        if profile_photo_base64:
            profile_photo_file = convert_base64_to_file(profile_photo_base64)
            user.profile_photo.save(name=profile_photo_file.name, content=profile_photo_file, save=True)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role_names = validated_data.pop('role_names', None)
        profile_photo_base64 = validated_data.pop('profile_photo_base64', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if role_names is not None:
            roles = Role.objects.filter(name__in=role_names)
            user.roles.set(roles)
        if profile_photo_base64:
            profile_photo_file = convert_base64_to_file(profile_photo_base64)
            user.profile_photo.save(name=profile_photo_file.name, content=profile_photo_file, save=True)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=40)

    def update(self, instance):
        new_token_instance = Token(
            created=datetime.utcnow(),
            key=Token.generate_key(),
            user=instance.user
        )
        instance.delete()
        new_token_instance.save()
        new_token_instance.token = new_token_instance.key
        return new_token_instance

    def create(self, validated_data):
        # This method will be used to fetch and update the token
        token_key = validated_data.get('token')
        try:
            token = Token.objects.get(key=token_key)
            return self.update(token)
        except Token.DoesNotExist:
            raise serializers.ValidationError(_('Invalid token.'))


class ProfileUserSerializer(serializers.ModelSerializer):
    """Serializer for the profile user object."""
    profile_photo_base64 = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'name',
            'cpf',
            'phone_number',
            'profile_photo',
            'profile_photo_base64',
        ]
        read_only_fields = ('profile_photo',)

    def update(self, instance, validated_data):
        profile_photo_base64 = validated_data.pop('profile_photo_base64', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_photo_base64:
            profile_photo_file = convert_base64_to_file(profile_photo_base64)
            instance.profile_photo.save(name=profile_photo_file.name, content=profile_photo_file, save=True)
        return instance


class RecoverPasswordUserSerializer(serializers.ModelSerializer):
    """Serializer for the recover password user object."""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
        ]


class ValidatePasswordCodeUserSerializer(serializers.ModelSerializer):
    """Serializer for the recover password user object."""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'recover_password_code'
        ]


class ChangePasswordCodeSerializer(serializers.ModelSerializer):
    """Serializer for the recover password user object."""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'recover_password_code'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
