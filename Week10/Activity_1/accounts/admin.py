from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['email', 'full_name', 'dob', 'role', 'is_active', 'date_joined']
    list_filter   = ['role', 'is_active']
    search_fields = ['email', 'full_name', 'username']
    ordering      = ['full_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Healthcare Profile', {'fields': ('full_name', 'dob', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Healthcare Profile', {'fields': ('full_name', 'dob', 'role')}),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display  = ['user', 'created_at', 'expires_at', 'is_used']
    list_filter   = ['is_used']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at', 'expires_at']
