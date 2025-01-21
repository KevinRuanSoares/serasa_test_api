"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
LOGIN_URL = reverse('user:login')
REFRESH_URL = reverse('user:login_refresh')
PROFILE_URL = reverse('user:profile')
RECOVER_PASSWORD_CODE_URL = reverse('user:recover_password_code')
VALIDATE_PASSWORD_CODE_URL = reverse('user:validate_password_code')
CHANGE_PASSWORD_CODE_URL = reverse('user:change_password_code')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features if the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
            'cpf': '433.982.130-65',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
            'cpf': '385.699.040-29'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
            'cpf': '385.699.040-29'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(
            email='test@example.com',
            password='goodpass',
            cpf='385.699.040-29',
            street='Rua Ernesto Lazzaron',
            postal_code='97070-415',
            city='Santa Maria',
            state='RS',
            phone_number='(47) 99214-8301',
        )

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
            cpf='433.982.130-65',
            street='Rua Ernesto Lazzaron',
            postal_code='97070-415',
            city='Santa Maria',
            state='RS',
            phone_number='(47) 99214-8301',
            profile_photo=None,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
            'cpf': self.user.cpf,
            'street': self.user.street,
            'postal_code': self.user.postal_code,
            'city': self.user.city,
            'state': self.user.state,
            'phone_number': self.user.phone_number,
            'profile_photo': None,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the profile endpoint."""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name'}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        old_token = Token.objects.create(user=self.user)
        old_created_time = old_token.created
        response = self.client.post(
            REFRESH_URL,
            {
                'token': old_token.key,
            }
        )
        self.assertEqual(response.status_code, 201)
        new_token = Token.objects.get(user=self.user)
        self.assertNotEqual(old_created_time, new_token.created)


class RecoverPasswordCodeUserViewTests(TestCase):
    """Test cases for RecoverPasswordCodeUserView."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()

    def test_recover_password_success(self):
        """Test generating a recover password code for an existing user."""
        res = self.client.post(RECOVER_PASSWORD_CODE_URL, {'email': self.user.email})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.recover_password_code)

    def test_recover_password_user_not_found(self):
        """Test generating a recover password code for a non-existent user."""
        res = self.client.post(RECOVER_PASSWORD_CODE_URL, {'email': 'nonexistent@example.com'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ValidatePasswordCodeViewTests(TestCase):
    """Test cases for ValidatePasswordCodeView."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            recover_password_code='1234',
            recover_password_code_attempts=0
        )
        self.client = APIClient()

    def test_password_code_validation_user_not_found(self):
        """Test validation for a non-existent user."""
        res = self.client.post(VALIDATE_PASSWORD_CODE_URL,
                               {'email': 'nonexistent@example.com', 'recover_password_code': '1234'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_password_code_validation_attempts_exceeded(self):
        """Test validation when maximum attempts are exceeded."""
        self.user.recover_password_code_attempts = 3
        self.user.save()
        res = self.client.post(VALIDATE_PASSWORD_CODE_URL,
                               {'email': self.user.email, 'recover_password_code': 'wrongcode'})
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_password_code_validation_incorrect_code(self):
        """Test validation with an incorrect code."""
        res = self.client.post(VALIDATE_PASSWORD_CODE_URL,
                               {'email': self.user.email, 'recover_password_code': 'wrongcode'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_code_validation_correct_code(self):
        """Test validation with a correct code."""
        res = self.client.post(VALIDATE_PASSWORD_CODE_URL,
                               {'email': self.user.email, 'recover_password_code': '1234'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.recover_password_code, '1234')
        self.assertEqual(self.user.recover_password_code_attempts, 0)


class ChangePasswordCodeViewTests(TestCase):
    """Test cases for ChangePasswordCodeView."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            recover_password_code='1234',
            recover_password_attempts=0
        )
        self.client = APIClient()

    def test_password_change_user_not_found(self):
        """Test password change for a non-existent user."""
        res = self.client.post(
            CHANGE_PASSWORD_CODE_URL,
            {
                'email': 'nonexistent@example.com',
                'recover_password_code': '1234',
                'password': 'newpassword'
            }
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_password_change_code_not_exist(self):
        """Test password change when the code does not exist."""
        self.user.recover_password_code = None
        self.user.save()
        res = self.client.post(
            CHANGE_PASSWORD_CODE_URL,
            {
                'email': self.user.email,
                'recover_password_code': '1234',
                'password': 'newpassword'
            }
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_password_change_attempts_exceeded(self):
        """Test password change when maximum attempts are exceeded."""
        self.user.recover_password_attempts = 4
        self.user.save()
        res = self.client.post(
            CHANGE_PASSWORD_CODE_URL,
            {'email': self.user.email, 'recover_password_code': 'wrongcode', 'password': 'newpassword'}
        )
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_password_change_incorrect_code(self):
        """Test password change with an incorrect code."""
        res = self.client.post(
            CHANGE_PASSWORD_CODE_URL,
            {'email': self.user.email, 'recover_password_code': 'wrongcode', 'password': 'newpassword'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_correct_code(self):
        """Test password change with a correct code."""
        res = self.client.post(
            CHANGE_PASSWORD_CODE_URL,
            {'email': self.user.email, 'recover_password_code': '1234', 'password': 'newpassword'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))
        self.assertIsNone(self.user.recover_password_code)
        self.assertEqual(self.user.recover_password_attempts, 0)
