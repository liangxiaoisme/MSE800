from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User, PasswordResetToken


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user sign-up. Validates passwords and creates the account."""

    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model  = User
        fields = ['email', 'username', 'full_name', 'dob', 'role', 'password', 'password2']
        extra_kwargs = {'role': {'required': False}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Validates email + password credentials."""

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account has been deactivated.')
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Read / update personal information (Full Name, DOB)."""

    class Meta:
        model  = User
        fields = ['id', 'email', 'username', 'full_name', 'dob', 'role', 'date_joined']
        read_only_fields = ['id', 'email', 'role', 'date_joined']


class ChangePasswordSerializer(serializers.Serializer):
    """Authenticated password change (requires current password)."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    """Accepts an email address and triggers reset token generation."""

    email = serializers.EmailField()

    def validate_email(self, value):
        # Don't reveal whether the email exists — just return it
        return value.lower()


class ResetPasswordSerializer(serializers.Serializer):
    """Validates the reset token and sets a new password."""

    token        = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, label='Confirm New Password')

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Passwords do not match.'})

        try:
            token_obj = PasswordResetToken.objects.select_related('user').get(token=data['token'])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid or expired reset link.'})

        if not token_obj.is_valid():
            raise serializers.ValidationError({'token': 'This reset link has expired or already been used.'})

        data['token_obj'] = token_obj
        return data
