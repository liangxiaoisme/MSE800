import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model for the Healthcare Compliance System.

    Extends Django's AbstractUser to add:
    - full_name  : required legal name (Week 10 Activity 1 requirement)
    - dob        : date of birth       (Week 10 Activity 1 requirement)
    - role       : STAFF or ADMIN for RBAC
    """

    class Role(models.TextChoices):
        STAFF = 'STAFF', 'Staff'
        ADMIN = 'ADMIN', 'Admin'

    full_name = models.CharField(max_length=100, verbose_name='Full Name')
    dob       = models.DateField(null=True, blank=False, verbose_name='Date of Birth')
    role      = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STAFF,
    )

    # Use email as the primary login identifier
    email    = models.EmailField(unique=True)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'dob']

    class Meta:
        verbose_name = 'User'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} <{self.email}> [{self.role}]'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


class PasswordResetToken(models.Model):
    """
    One-time token for the Forgot Password flow.
    Expires after PASSWORD_RESET_TIMEOUT_MINUTES (default 30 min).
    """
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token      = models.CharField(max_length=64, unique=True, editable=False)
    expires_at = models.DateTimeField(editable=False)
    is_used    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Password Reset Token'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        if not self.expires_at:
            from django.conf import settings
            minutes = getattr(settings, 'PASSWORD_RESET_TIMEOUT_MINUTES', 30)
            self.expires_at = timezone.now() + timedelta(minutes=minutes)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        status = 'valid' if self.is_valid() else 'expired/used'
        return f'ResetToken({self.user.email}, {status})'
