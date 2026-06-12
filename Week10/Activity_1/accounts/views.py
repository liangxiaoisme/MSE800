from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, PasswordResetToken
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


# ─────────────────────────────────────────────────────────────────────────────
# HTML page views (served to the browser)
# ─────────────────────────────────────────────────────────────────────────────

def login_page(request):
    return render(request, 'accounts/login.html')

def signup_page(request):
    return render(request, 'accounts/signup.html')

def profile_page(request):
    return render(request, 'accounts/profile.html')

def forgot_password_page(request):
    return render(request, 'accounts/forgot_password.html')

def reset_password_page(request):
    token = request.GET.get('token', '')
    return render(request, 'accounts/reset_password.html', {'token': token})


# ─────────────────────────────────────────────────────────────────────────────
# API: Register
# POST /api/auth/register/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Create a new user account.

    Body: email, username, full_name, dob (YYYY-MM-DD), password, password2, role (optional)
    Returns: user info + JWT tokens
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    tokens = _get_tokens(user)
    return Response(
        {
            'message': 'Account created successfully.',
            'user': UserProfileSerializer(user).data,
            **tokens,
        },
        status=status.HTTP_201_CREATED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# API: Login
# POST /api/auth/login/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate with email + password.

    Returns: user info + JWT access & refresh tokens
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    tokens = _get_tokens(user)
    return Response(
        {
            'message': 'Login successful.',
            'user': UserProfileSerializer(user).data,
            **tokens,
        }
    )


# ─────────────────────────────────────────────────────────────────────────────
# API: Profile — view & update personal information
# GET  /api/auth/me/
# PUT  /api/auth/me/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    GET  → returns current user's full_name, dob, email, role
    PUT  → updates full_name and/or dob
    """
    user = request.user

    if request.method == 'GET':
        return Response(UserProfileSerializer(user).data)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': 'Profile updated.', 'user': serializer.data})


# ─────────────────────────────────────────────────────────────────────────────
# API: Change Password (authenticated)
# POST /api/auth/change-password/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()
    return Response({'message': 'Password changed successfully.'})


# ─────────────────────────────────────────────────────────────────────────────
# API: Forgot Password — send reset email
# POST /api/auth/forgot-password/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Accepts an email. If the account exists, emails a reset link.
    Always returns 200 to avoid revealing whether an account exists.
    """
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email=email)
        # Invalidate any previous unused tokens
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

        token_obj = PasswordResetToken.objects.create(user=user)

        # Build reset URL (uses HTTP_HOST from request for flexibility)
        host = request.get_host()
        reset_url = f'http://{host}/api/auth/reset-password-page/?token={token_obj.token}'

        send_mail(
            subject='Healthcare System — Password Reset Request',
            message=(
                f'Hi {user.full_name},\n\n'
                f'Click the link below to reset your password (valid for 30 minutes):\n\n'
                f'{reset_url}\n\n'
                f'If you did not request this, please ignore this email.\n\n'
                f'— Healthcare Compliance Team'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
    except User.DoesNotExist:
        pass  # Silent — do not reveal account existence

    return Response(
        {'message': 'If that email is registered, a reset link has been sent.'}
    )


# ─────────────────────────────────────────────────────────────────────────────
# API: Reset Password — use token to set new password
# POST /api/auth/reset-password/
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Validates the one-time token and sets the new password.
    Body: token, new_password, new_password2
    """
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token_obj = serializer.validated_data['token_obj']
    user = token_obj.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()

    token_obj.is_used = True
    token_obj.save()

    return Response({'message': 'Password reset successfully. You can now log in.'})


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access':  str(refresh.access_token),
        'refresh': str(refresh),
    }
