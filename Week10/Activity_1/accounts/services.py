"""
Service Layer — all business logic lives here.

Views call services. Services call models.
Neither models nor serializers contain business logic.

                 Request
                    │
              ┌─────▼──────┐
              │   views/   │  ← thin: receive, validate, respond
              └─────┬──────┘
                    │ calls
              ┌─────▼──────┐
              │  services  │  ← business logic (THIS FILE)
              └─────┬──────┘
                    │ reads/writes
              ┌─────▼──────┐
              │   models   │  ← data structure only
              └────────────┘
"""

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PasswordResetToken, User


class AuthService:
    """Handles registration, login tokens, and password operations."""

    @staticmethod
    def generate_tokens(user) -> dict:
        """Return a JWT access + refresh token pair for the given user."""
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def change_password(user, new_password: str) -> None:
        """Set a new password for an already-authenticated user."""
        user.set_password(new_password)
        user.save()


class PasswordResetService:
    """Handles the forgot-password / reset-password flow."""

    @staticmethod
    def send_reset_email(email: str, host: str) -> None:
        """
        Create a one-time reset token and email the link.
        Always returns silently if the email is not registered
        (prevents account-enumeration attacks).
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return

        # Invalidate all previous unused tokens for this user
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

        token_obj = PasswordResetToken.objects.create(user=user)
        reset_url = f"http://{host}/api/auth/reset-password-page/?token={token_obj.token}"

        send_mail(
            subject="Healthcare System — Password Reset Request",
            message=(
                f"Hi {user.full_name},\n\n"
                f"Click the link below to reset your password "
                f"(valid for 30 minutes):\n\n"
                f"{reset_url}\n\n"
                f"If you did not request this, please ignore this email.\n\n"
                f"— Healthcare Compliance Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

    @staticmethod
    def consume_token(token_str: str, new_password: str) -> None:
        """
        Validate the reset token, apply the new password, mark the token used.
        Raises ValidationError if the token is missing, expired, or already used.
        """
        try:
            token_obj = PasswordResetToken.objects.select_related("user").get(
                token=token_str
            )
        except PasswordResetToken.DoesNotExist:
            raise ValidationError({"token": "Invalid or expired reset link."})

        if not token_obj.is_valid():
            raise ValidationError(
                {"token": "This reset link has expired or already been used."}
            )

        user = token_obj.user
        user.set_password(new_password)
        user.save()

        token_obj.is_used = True
        token_obj.save()
