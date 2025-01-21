"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an emailis successful."""
        email = 'test@example.com'
        password = 'testpass123'
        cpf = '385.699.040-29'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            cpf=cpf,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com', '647.494.730-65'],
            ['Test2@Example.com', 'Test2@example.com', '239.071.740-38'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com', '812.293.180-46'],
            ['test4@EXAMPLE.COM', 'test4@example.com', '617.697.510-76'],
        ]
        for email, expected, cpf in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                'sample123',
                cpf=cpf
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                'test123',
                cpf='010.466.550-51'
            )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
