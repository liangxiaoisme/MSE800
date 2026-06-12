"""
Serializers — one responsibility: validate and transform request data.

Serializers do NOT query the database for business purposes,
do NOT send emails, and do NOT generate tokens.
All of that belongs in services.py.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Validate sign-up fields and create the new user account."""

    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model  = User
        fields = ["email", "username", "full_name", "dob", "role", "password", "password2"]
        extra_kwargs = {"role": {"required": False}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Validate email + password credentials."""

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")
        data["user"] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Read / update personal information (Full Name, DOB)."""

    class Meta:
        model  = User
        fields = ["id", "email", "username", "full_name", "dob", "role", "date_joined"]
        read_only_fields = ["id", "email", "role", "date_joined"]


class ChangePasswordSerializer(serializers.Serializer):
    """Validate an authenticated password change (requires current password)."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    """Accept an email address for the forgot-password flow."""

    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Validate the reset form fields only.
    Token existence and expiry are checked in PasswordResetService.consume_token().
    """

    token         = serializers.CharField()
    new_password  = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, label="Confirm New Password")

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})
        return data
