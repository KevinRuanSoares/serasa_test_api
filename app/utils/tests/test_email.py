from django.test import TestCase
from django.core import mail
from django.contrib.auth import (
    get_user_model,
)
from utils.email import send_password_reset_code
from django.utils.translation import gettext_lazy as _


class SendPasswordResetCodeTestCase(TestCase):

    def setUp(self):
        # Set up a test user
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            name='testuser',
            password='password123',
            recover_password_code='123456'
        )

    def test_send_password_reset_code(self):
        # Call the function
        send_password_reset_code(self.user)

        # Check the outbox
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Check email properties
        self.assertEqual(email.subject, _('Your code to generate a new password!'))
        self.assertIn('123456', email.body)  # Checking if the code is in the email body
        self.assertIn(self.user.email, email.to)
