from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # ── HTML pages ────────────────────────────────────────────────────────
    path('login-page/',          views.login_page,           name='login-page'),
    path('signup-page/',         views.signup_page,          name='signup-page'),
    path('profile-page/',        views.profile_page,         name='profile-page'),
    path('forgot-password-page/', views.forgot_password_page, name='forgot-password-page'),
    path('reset-password-page/', views.reset_password_page,  name='reset-password-page'),

    # ── REST API endpoints ────────────────────────────────────────────────
    path('register/',        views.register,        name='register'),
    path('login/',           views.login,           name='login'),
    path('token/refresh/',   TokenRefreshView.as_view(), name='token-refresh'),
    path('me/',              views.profile,         name='profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/',  views.reset_password,  name='reset-password'),
]
