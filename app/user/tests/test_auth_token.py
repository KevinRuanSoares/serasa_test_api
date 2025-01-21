from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from user.auth import CheckTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import datetime

LOGIN_URL = reverse('user:login')


class CheckTokenAuthenticationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@example.com',
            name='testuser',
        )
        self.token = Token.objects.create(user=self.user)

    def test_valid_token(self):
        authentication = CheckTokenAuthentication()
        user, token = authentication.authenticate_credentials(self.token.key)
        self.assertEqual(user, self.user)
        self.assertEqual(token, self.token)

    def test_invalid_token(self):
        authentication = CheckTokenAuthentication()
        with self.assertRaises(AuthenticationFailed) as context:
            authentication.authenticate_credentials('invalidtoken')
        self.assertEqual(str(context.exception), 'Token inválido.')

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        authentication = CheckTokenAuthentication()
        with self.assertRaises(AuthenticationFailed) as context:
            authentication.authenticate_credentials(self.token.key)
        self.assertEqual(str(context.exception), 'Usuário inativo ou excluído.')

    def test_expired_token(self):
        settings.AUTH_TOKEN_EXPIRATION_TIME = 1
        self.token.created = datetime.datetime(
            2022, 12, 29,
            tzinfo=datetime.timezone.utc
        )
        self.token.save()

        authentication = CheckTokenAuthentication()
        with self.assertRaises(AuthenticationFailed) as context:
            authentication.authenticate_credentials(self.token.key)
        self.assertEqual(str(context.exception), 'O token expirou.')
