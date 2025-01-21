"""
Check for user token
"""
import pytz
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class CheckTokenAuthentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('Inactive or deleted user.'))

        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(
            days=settings.AUTH_TOKEN_EXPIRATION_TIME
        ):
            raise AuthenticationFailed(_('The token has expired.'))
        return token.user, token
