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


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'name',
            'cpf',
            'street',
            'postal_code',
            'city',
            'state',
            'phone_number'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

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

    def update(self, instance, validated_data):
        instance.created = datetime.utcnow()  # Set created to None
        instance.save()
        instance.token = instance.key
        return instance

    def create(self, validated_data):
        # This method will be used to fetch and update the token
        token_key = validated_data.get('token')
        try:
            token = Token.objects.get(key=token_key)
            return self.update(token, validated_data)
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
            'street',
            'postal_code',
            'city',
            'state',
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
