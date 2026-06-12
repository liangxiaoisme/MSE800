# Week 10 — Activity 1: Login & Signup System

**Project:** Intelligent Healthcare Compliance & Safety Management System  
**Group:** W · Abu Sufian · Xiao Liang · MSE800 Week 10

---

## Overview

A full-featured authentication module built with **Django + Django REST Framework**.  
It provides user account management for the Healthcare Compliance System, including
sign-up, sign-in, personal information management, and a forgot-password flow.

### Features

| Feature | Description |
|---|---|
| **Sign Up** | Register with Full Name, Date of Birth, email, username, role |
| **Login** | Email + password authentication returning JWT tokens |
| **My Profile** | View and edit Full Name, Date of Birth, Username |
| **Change Password** | Authenticated password update (requires current password) |
| **Forgot Password** | Sends a 30-minute one-time reset link via email |
| **Reset Password** | Validates token and sets new password |

---

## Database Tables

| Table | Purpose |
|---|---|
| `accounts_user` | Stores all user accounts (extends Django's AbstractUser) |
| `accounts_passwordresettoken` | One-time tokens for the Forgot Password flow |

### `accounts_user` fields

| Field | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `full_name` | CharField(100) | **Required** — legal full name |
| `dob` | DateField | **Required** — date of birth |
| `email` | EmailField UNIQUE | Used as login identifier |
| `username` | CharField UNIQUE | Display name |
| `password` | CharField | Bcrypt hash (Django built-in) |
| `role` | CharField | `STAFF` or `ADMIN` |
| `is_active` | Boolean | Account enabled/disabled |
| `date_joined` | DateTimeField | Auto-set on creation |

### `accounts_passwordresettoken` fields

| Field | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `user_id` | FK → accounts_user | Cascade delete |
| `token` | CharField UNIQUE | URL-safe random 32-byte token |
| `expires_at` | DateTimeField | 30 minutes after creation |
| `is_used` | Boolean | Consumed after one use |
| `created_at` | DateTimeField | Auto-set |

---

## Project Structure

```
Week10/Activity_1/
├── manage.py
├── requirements.txt
├── healthcare_auth/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                 # Authentication app
│   ├── models.py             # User + PasswordResetToken
│   ├── serializers.py        # Input validation & transformation
│   ├── views.py              # API logic + HTML page views
│   ├── urls.py               # URL routing
│   └── admin.py              # Django admin configuration
└── templates/
    └── accounts/
        ├── base.html         # Shared navbar + layout
        ├── login.html        # Sign In page
        ├── signup.html       # Register page
        ├── profile.html      # Profile + Change Password page
        ├── forgot_password.html
        └── reset_password.html
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Public | Create new account |
| `POST` | `/api/auth/login/` | Public | Login, returns JWT |
| `POST` | `/api/auth/token/refresh/` | Public | Refresh access token |
| `GET` | `/api/auth/me/` | JWT | Get current user profile |
| `PUT` | `/api/auth/me/` | JWT | Update full_name / dob |
| `POST` | `/api/auth/change-password/` | JWT | Change password |
| `POST` | `/api/auth/forgot-password/` | Public | Send password reset email |
| `POST` | `/api/auth/reset-password/` | Public | Reset password with token |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations accounts
python manage.py migrate

# 3. (Optional) Create superuser for admin panel
python manage.py createsuperuser

# 4. Start development server
python manage.py runserver
```

Then open: **http://127.0.0.1:8000**

> **Forgot Password emails** are printed to the terminal (console backend).  
> Look for the reset URL in your terminal output.

---

## Design Decisions

- **AbstractUser** — Django's built-in user model is extended rather than replaced,
  preserving all built-in admin and auth features while adding healthcare-specific fields.
- **Email as login** — `USERNAME_FIELD = 'email'` ensures unique, professional login identifiers.
- **JWT (Simple JWT)** — Stateless tokens; access token expires in 1 hour, refresh in 7 days.
- **One-time reset tokens** — `PasswordResetToken` records are invalidated after use or
  after 30 minutes, preventing token reuse attacks.
- **Silent email check** — `/forgot-password/` always returns 200 regardless of whether
  the email exists, preventing account enumeration.
- **Console email backend** — No SMTP configuration required for development; swap to
  `django.core.mail.backends.smtp.EmailBackend` for production.
