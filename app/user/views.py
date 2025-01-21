"""
Views for the user API.
"""

import threading
from random import randint
from django.contrib.auth import (
    get_user_model,
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status

from user.serializers import (
    UserSerializer,
    ProfileUserSerializer,
    AuthTokenSerializer,
    TokenRefreshSerializer,
    RecoverPasswordUserSerializer,
    ValidatePasswordCodeUserSerializer,
    ChangePasswordCodeSerializer,
)
from user.auth import (
    CheckTokenAuthentication,
)
from utils.email import send_password_reset_code


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RefreshTokenView(generics.CreateAPIView):
    serializer_class = TokenRefreshSerializer


class ProfileUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ProfileUserSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class RecoverPasswordCodeUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = RecoverPasswordUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.data.get("email"))
        except ObjectDoesNotExist:
            return Response({"detail": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)
        code = str(randint(1111, 9999))
        user.recover_password_code = code
        user.save()
        thread = threading.Thread(target=send_password_reset_code, kwargs={'user': user})
        thread.start()
        return Response(status=status.HTTP_200_OK)


class ValidatePasswordCodeView(generics.CreateAPIView):
    serializer_class = ValidatePasswordCodeUserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        input_code = request.data.get("recover_password_code")

        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'detail': _("User not found.")}, status=status.HTTP_404_NOT_FOUND)

        user.recover_password_code_attempts = user.recover_password_code_attempts+1
        user.save()

        if user.recover_password_code_attempts >= 3:
            user.recover_password_code_attempts = 0
            user.recover_password_code = None
            user.save()
            return Response({'detail': _("Attempts exceeded.")}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if user.recover_password_code != input_code:
            return Response({'detail': _("Invalid Code.")}, status=status.HTTP_400_BAD_REQUEST)

        user.recover_password_code = str(randint(1111, 9999))
        user.recover_password_code_attempts = 0
        user.save()
        return Response({"recover_password_code": user.recover_password_code}, status=status.HTTP_200_OK)


class ChangePasswordCodeView(generics.CreateAPIView):
    serializer_class = ChangePasswordCodeSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        recover_password_code = request.data.get("recover_password_code")
        password = request.data.get("password")

        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'detail': _("User not found.")}, status=status.HTTP_404_NOT_FOUND)

        if not user.recover_password_code:
            return Response({'detail': _("Code does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        user.recover_password_attempts += 1
        user.save()

        if user.recover_password_attempts > 3:
            user.recover_password_attempts = 0
            user.recover_password_code = None
            user.save()
            return Response({'detail': _("Attempts exceeded.")}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if recover_password_code == user.recover_password_code:
            user.set_password(password)
            user.recover_password_code_check = False
            user.recover_password_code = None
            user.recover_password_attempts = 0
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response({'detail': _("Invalid code.")}, status=status.HTTP_400_BAD_REQUEST)
