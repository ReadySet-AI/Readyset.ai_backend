from enum import Enum

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models

from addons.mixins import TimeStampMixin


class Roles(Enum):
    Global_Admin = "Global Admin"
    Company_Admin = "Company Admin"
    Mentor = "Mentor"
    Newcomer = "Newcomer"


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(TimeStampMixin, AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])
    department = models.CharField(max_length=220, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[(role.name, role.value) for role in Roles],
        null=False,
        blank=False,
        default=None,
    )
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
