"""
Views — two clearly separated sections:

  SECTION 1 · Page Views
    Return HTML templates. No business logic.

  SECTION 2 · API Views
    Receive request → validate with serializer → call service → return Response.
    Each function is intentionally short: ≤ 8 lines of logic.

Business logic lives entirely in services.py, NOT here.
"""

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
)
from .services import AuthService, PasswordResetService


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 · Page Views
# Responsibility: render the correct HTML template, nothing else.
# ─────────────────────────────────────────────────────────────────────────────

def login_page(request):
    return render(request, "accounts/login.html")


def signup_page(request):
    return render(request, "accounts/signup.html")


def profile_page(request):
    return render(request, "accounts/profile.html")


def forgot_password_page(request):
    return render(request, "accounts/forgot_password.html")


def reset_password_page(request):
    token = request.GET.get("token", "")
    return render(request, "accounts/reset_password.html", {"token": token})


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 · API Views
# Responsibility: validate input → call service → return Response.
# No business logic, no direct model access, no email sending here.
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(
        {
            "message": "Account created successfully.",
            "user": UserProfileSerializer(user).data,
            **AuthService.generate_tokens(user),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    return Response(
        {
            "message": "Login successful.",
            "user": UserProfileSerializer(user).data,
            **AuthService.generate_tokens(user),
        }
    )


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        return Response(UserProfileSerializer(request.user).data)

    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Profile updated.", "user": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    AuthService.change_password(request.user, serializer.validated_data["new_password"])
    return Response({"message": "Password changed successfully."})


@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    PasswordResetService.send_reset_email(
        email=serializer.validated_data["email"],
        host=request.get_host(),
    )
    return Response({"message": "If that email is registered, a reset link has been sent."})


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    PasswordResetService.consume_token(
        token_str=serializer.validated_data["token"],
        new_password=serializer.validated_data["new_password"],
    )
    return Response({"message": "Password reset successfully. You can now log in."})
