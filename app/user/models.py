"""
Database models.
"""
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from utils import validate_cpf


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(max_length=255, unique=True, error_messages={
        'unique': _("User with this email already exists.")})
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    cpf = models.CharField(max_length=14, unique=True, validators=[
        validate_cpf
    ], error_messages={'unique': _("User with this cpf already exists.")})

    street = models.CharField(max_length=255, null=True, blank=False)
    postal_code = models.CharField(max_length=15, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    state = models.CharField(max_length=20, null=True, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=False)

    recover_password_code = models.CharField(max_length=6, blank=True, null=True)
    recover_password_code_check = models.BooleanField(default=False)
    recover_password_code_attempts = models.IntegerField(default=0)
    recover_password_attempts = models.IntegerField(default=0)
    profile_photo = models.FileField(upload_to='uploads/profile_photos/', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
