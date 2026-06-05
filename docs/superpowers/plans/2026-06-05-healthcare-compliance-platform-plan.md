# Healthcare Compliance & Safety Management Platform — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working MVP of an AI-powered healthcare compliance platform with training, compliance monitoring, incident reporting, and a RAG chatbot, deployed across Vercel + Render + Supabase.

**Architecture:** Django REST API (Render) serves training/compliance/incidents/chatbot endpoints backed by PostgreSQL+pgvector (Supabase). React SPA (Vercel) consumes them via JWT-authenticated Axios calls. RAG pipeline uses fastembed (bge-small-en, 384-dim) for chunk embeddings stored in pgvector, and OpenRouter's Llama 4 Maverick free tier for answer generation.

**Tech Stack:** Django 5 · DRF · djangorestframework-simplejwt · psycopg · pgvector · fastembed (BAAI/bge-small-en) · httpx · django-cors-headers · React 18 · Vite · React Router · Axios

**Note:** The spec explicitly excludes unit/integration tests for MVP speed. Steps are implementation-only.

---

## File Map

```
healthcare_platform/
├── backend/
│   ├── config/              # Django settings (12-factor env vars), root URL conf, wsgi
│   ├── accounts/            # Custom User model (role: STAFF|ADMIN), JWT auth, user endpoints
│   ├── training/            # Module, Question, Enrollment models + CRUD views
│   ├── compliance/          # Requirement, ComplianceRecord models + list/detail views
│   ├── incidents/           # Incident model + create (staff) / list+update (admin) views
│   ├── chatbot/             # Document, Chunk models + ask endpoint + RAG pipeline + management commands
│   ├── seed/                # 5 healthcare compliance plain-text documents + Django fixtures
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── index.html, package.json, vite.config.js
│   └── src/
│       ├── main.jsx, App.jsx
│       ├── api/client.js        # Axios instance, JWT interceptor
│       ├── auth/                # LoginPage, AuthContext (token + user + role), ProtectedRoute
│       ├── pages/               # Dashboard, TrainingList, TrainingDetail, ComplianceList, IncidentList, IncidentForm
│       ├── components/          # Layout (sidebar + header), ChatWidget (floating button + slide-out panel)
│       └── styles/global.css    # Minimal hand-rolled CSS
└── README.md
```

---

## Phase 1: Scaffold Backend + Models + Seed Data

### Task 1.1: Create project root and README

**Files:**
- Create: `healthcare_platform/README.md`

- [ ] **Step 1: Scaffold directory**

```bash
mkdir -p healthcare_platform/backend healthcare_platform/frontend/src
```

- [ ] **Step 2: Write project README**

Create `healthcare_platform/README.md`:

```markdown
# Intelligent Healthcare Compliance & Safety Management Platform

AI-powered platform for healthcare staff safety training, compliance monitoring,
incident reporting, and an intelligent RAG chatbot assistant.

## Stack

- **Frontend:** React 18 + Vite (deployed on Vercel)
- **Backend:** Django 5 + Django REST Framework (deployed on Render)
- **Database:** PostgreSQL + pgvector (Supabase)
- **AI:** Llama 4 Maverick via OpenRouter (RAG-powered chatbot)

## Quickstart

See `docs/superpowers/specs/2026-06-05-healthcare-compliance-platform-design.md`
for the full design spec.
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/README.md
git commit -m "feat: add healthcare platform README"
```

### Task 1.2: Scaffold Django project

**Files:**
- Create: `healthcare_platform/backend/manage.py`
- Create: `healthcare_platform/backend/config/__init__.py`
- Create: `healthcare_platform/backend/config/settings.py`
- Create: `healthcare_platform/backend/config/urls.py`
- Create: `healthcare_platform/backend/config/wsgi.py`
- Create: `healthcare_platform/backend/requirements.txt`

- [ ] **Step 1: Create manage.py**

Create `healthcare_platform/backend/manage.py`:

```python
#!/usr/bin/env python
"""Django's command-line utility."""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

- [ ] **Step 2: Create config/__init__.py**

Create `healthcare_platform/backend/config/__init__.py` (empty file):

```python
```

- [ ] **Step 3: Create config/settings.py**

Create `healthcare_platform/backend/config/settings.py`:

```python
import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-change-me")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Local
    "accounts",
    "training",
    "compliance",
    "incidents",
    "chatbot",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database: PostgreSQL via DATABASE_URL env var; fallback to SQLite for local dev
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import re
    match = re.match(r"postgres(?:ql)?://([^:]+):([^@]+)@([^:/]+):?(\d+)?/(.+)", DATABASE_URL)
    if match:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": match.group(5),
                "USER": match.group(1),
                "PASSWORD": match.group(2),
                "HOST": match.group(3),
                "PORT": match.group(4) or "5432",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ORIGINS", "http://localhost:5173"
).split(",")

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

- [ ] **Step 4: Create config/urls.py**

Create `healthcare_platform/backend/config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/training/", include("training.urls")),
    path("api/compliance/", include("compliance.urls")),
    path("api/incidents/", include("incidents.urls")),
    path("api/chatbot/", include("chatbot.urls")),
]
```

- [ ] **Step 5: Create config/wsgi.py**

Create `healthcare_platform/backend/config/wsgi.py`:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
```

- [ ] **Step 6: Create requirements.txt**

Create `healthcare_platform/backend/requirements.txt`:

```
Django>=5.0,<6.0
djangorestframework>=3.15,<4.0
djangorestframework-simplejwt>=5.4,<6.0
django-cors-headers>=4.5,<5.0
psycopg[binary]>=3.2,<4.0
pgvector>=0.3,<1.0
fastembed>=0.4,<1.0
httpx>=0.28,<1.0
gunicorn>=23.0,<24.0
```

- [ ] **Step 7: Install dependencies and verify Django boots**

```bash
cd healthcare_platform/backend && pip install -r requirements.txt && python manage.py check
```

Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 8: Commit**

```bash
git add healthcare_platform/backend/
git commit -m "feat: scaffold Django project with settings and requirements"
```

### Task 1.3: Create accounts app (custom User model)

**Files:**
- Create: `healthcare_platform/backend/accounts/__init__.py`
- Create: `healthcare_platform/backend/accounts/models.py`

- [ ] **Step 1: Create empty __init__.py**

Create `healthcare_platform/backend/accounts/__init__.py`:

```python
```

- [ ] **Step 2: Create accounts/models.py**

Create `healthcare_platform/backend/accounts/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STAFF = "STAFF", "Staff"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.STAFF
    )
```

- [ ] **Step 3: Run migrations**

```bash
cd healthcare_platform/backend && python manage.py makemigrations accounts && python manage.py migrate
```

Expected: creates `accounts_user` table, no errors.

- [ ] **Step 4: Commit**

```bash
git add healthcare_platform/backend/accounts/
git commit -m "feat: add custom User model with STAFF/ADMIN roles"
```

### Task 1.4: Create training app (models)

**Files:**
- Create: `healthcare_platform/backend/training/__init__.py`
- Create: `healthcare_platform/backend/training/models.py`

- [ ] **Step 1: Create training/models.py**

Create `healthcare_platform/backend/training/models.py`:

```python
from django.conf import settings
from django.db import models


class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(help_text="Markdown body of the training material")
    pass_mark = models.IntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    options = models.JSONField(help_text='["Option A", "Option B", "Option C", "Option D"]')
    correct_index = models.IntegerField(help_text="0-based index of the correct option")

    def __str__(self):
        return f"Q: {self.text[:60]}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "Not Started"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    score = models.IntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "module")

    def __str__(self):
        return f"{self.user.username} — {self.module.title}"
```

- [ ] **Step 2: Run migrations**

```bash
cd healthcare_platform/backend && python manage.py makemigrations training && python manage.py migrate
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/backend/training/
git commit -m "feat: add training models (Module, Question, Enrollment)"
```

### Task 1.5: Create compliance app (models)

**Files:**
- Create: `healthcare_platform/backend/compliance/__init__.py`
- Create: `healthcare_platform/backend/compliance/models.py`

- [ ] **Step 1: Create compliance/models.py**

Create `healthcare_platform/backend/compliance/models.py`:

```python
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Requirement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    frequency_days = models.IntegerField(help_text="How often (days) staff must renew this requirement")

    def __str__(self):
        return self.title


class ComplianceRecord(models.Model):
    class Status(models.TextChoices):
        COMPLIANT = "COMPLIANT", "Compliant"
        DUE = "DUE", "Due"
        OVERDUE = "OVERDUE", "Overdue"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    last_completed_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "requirement")

    def compute_status(self):
        """Compute compliance status on read — no cron needed."""
        if self.last_completed_at and self.due_at:
            now = timezone.now()
            if now <= self.due_at:
                return self.Status.COMPLIANT
            elif now <= self.due_at + timedelta(days=30):
                return self.Status.DUE
            else:
                return self.Status.OVERDUE
        return self.Status.OVERDUE

    def __str__(self):
        return f"{self.user.username} — {self.requirement.title}"
```

- [ ] **Step 2: Run migrations**

```bash
cd healthcare_platform/backend && python manage.py makemigrations compliance && python manage.py migrate
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/backend/compliance/
git commit -m "feat: add compliance models (Requirement, ComplianceRecord)"
```

### Task 1.6: Create incidents app (models)

**Files:**
- Create: `healthcare_platform/backend/incidents/__init__.py`
- Create: `healthcare_platform/backend/incidents/models.py`

- [ ] **Step 1: Create incidents/models.py**

Create `healthcare_platform/backend/incidents/models.py`:

```python
from django.conf import settings
from django.db import models


class Incident(models.Model):
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        RESOLVED = "RESOLVED", "Resolved"

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.LOW)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
```

- [ ] **Step 2: Run migrations**

```bash
cd healthcare_platform/backend && python manage.py makemigrations incidents && python manage.py migrate
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/backend/incidents/
git commit -m "feat: add incidents model"
```

### Task 1.7: Create chatbot app (models)

**Files:**
- Create: `healthcare_platform/backend/chatbot/__init__.py`
- Create: `healthcare_platform/backend/chatbot/models.py`

- [ ] **Step 1: Create chatbot/models.py**

Create `healthcare_platform/backend/chatbot/models.py`:

```python
from django.conf import settings
from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=200, help_text="e.g. 'WHO Hand Hygiene Guidelines 2024'")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    content = models.TextField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=384)

    class Meta:
        ordering = ["document", "chunk_index"]

    def __str__(self):
        return f"{self.document.title} chunk #{self.chunk_index}"
```

- [ ] **Step 2: Ensure pgvector extension is enabled**

Create `healthcare_platform/backend/chatbot/migrations/__init__.py`:

```python
```

Then create `healthcare_platform/backend/chatbot/migrations/0001_initial_setup.py`:

```python
from django.db import migrations
from pgvector.django import VectorExtension

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [VectorExtension()]
```

- [ ] **Step 3: Run migrations**

```bash
cd healthcare_platform/backend && python manage.py makemigrations chatbot && python manage.py migrate
```

Note: if running against SQLite locally, pgvector fields won't work. Use `DATABASE_URL` pointing to a real Postgres+pgvector instance for chatbot features. For Phase 1 model scaffolding, the migration will still be created.

- [ ] **Step 4: Commit**

```bash
git add healthcare_platform/backend/chatbot/
git commit -m "feat: add chatbot models (Document, Chunk with pgvector)"
```

### Task 1.8: Create seed data

**Files:**
- Create: `healthcare_platform/backend/seed/management/commands/seed_data.py` (or `seed/` at project level)
- Create: `healthcare_platform/backend/seed/docs/` with 5 `.txt` files

Since fixture loading is simpler for an MVP, we'll use a management command.

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p healthcare_platform/backend/seed/management/commands
mkdir -p healthcare_platform/backend/seed/docs
```

Create `healthcare_platform/backend/seed/__init__.py` (empty file needed for Django to discover the management command):

```python
```

- [ ] **Step 2: Create seed docs (5 healthcare compliance documents)**

Create `healthcare_platform/backend/seed/docs/hand_hygiene.txt`:

```
Hand Hygiene Protocol
=====================
Proper hand hygiene is the single most important measure to prevent healthcare-associated infections.
Staff must perform hand hygiene:
1. Before touching a patient
2. Before clean/aseptic procedures
3. After body fluid exposure risk
4. After touching a patient
5. After touching patient surroundings
Use alcohol-based hand rub for 20-30 seconds. Use soap and water when hands are visibly soiled or after contact with bodily fluids.
Compliance is audited monthly. Non-compliance results in mandatory retraining.
```

Create `healthcare_platform/backend/seed/docs/infection_control.txt`:

```
Infection Control and Prevention
================================
All healthcare staff must follow standard infection control precautions:
- Wear appropriate PPE (gloves, gowns, mask, eye protection) based on risk assessment
- Dispose of sharps immediately in designated puncture-resistant containers
- Never recap needles
- Handle soiled linen with minimal agitation
- Clean and disinfect patient equipment between uses
- Report any breach in infection control immediately via the incident reporting system
Annual infection control training is mandatory for all clinical staff.
```

Create `healthcare_platform/backend/seed/docs/incident_protocol.txt`:

```
Incident Reporting Protocol
============================
Any safety incident must be reported within 24 hours of occurrence. Incidents include:
- Patient falls or injuries
- Medication errors
- Needlestick or sharps injuries
- Equipment malfunction causing harm
- Workplace violence or aggression
- Exposure to hazardous substances
The report must include: what happened, where, when, who was involved, and immediate actions taken.
The incident is reviewed by the safety officer within 48 hours. Corrective actions are documented and tracked.
```

Create `healthcare_platform/backend/seed/docs/ppe_guidelines.txt`:

```
Personal Protective Equipment (PPE) Guidelines
===============================================
PPE is the last line of defense against workplace hazards. Selection depends on the task and risk:
- Gloves: for any contact with blood, body fluids, mucous membranes, or non-intact skin
- Gowns: when clothing may be splashed or contaminated
- Surgical masks: for droplet precautions (influenza, meningitis)
- N95 respirators: for airborne precautions (tuberculosis, measles, COVID-19)
- Eye protection: when splashes or sprays are anticipated
PPE must be donned before entering the patient zone and removed before leaving.
Sequence for donning: gown → mask → eye protection → gloves
Sequence for removal: gloves → eye protection → gown → mask → hand hygiene
```

Create `healthcare_platform/backend/seed/docs/workplace_safety.txt`:

```
Workplace Health and Safety
============================
Healthcare workers face unique workplace hazards. Key safety practices:
- Use proper body mechanics and lifting equipment when moving patients
- Report defective equipment immediately and tag it out of service
- Know the location of fire exits, extinguishers, and emergency assembly points
- Participate in emergency drills (fire, earthquake, code blue) as scheduled
- Maintain clear corridors and walkways — no trip hazards
- Follow electrical safety: no daisy-chained power strips, report frayed cords
- Violence prevention: de-escalation training, panic buttons in high-risk areas, never work alone in isolated areas
Quarterly safety walkthroughs are conducted by the facility safety officer.
```

- [ ] **Step 3: Create seed data management command**

Create `healthcare_platform/backend/seed/management/__init__.py` (empty):

```python
```

Create `healthcare_platform/backend/seed/management/commands/__init__.py` (empty):

```python
```

Create `healthcare_platform/backend/seed/management/commands/seed_data.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from training.models import Module, Question, Enrollment
from compliance.models import Requirement, ComplianceRecord
from incidents.models import Incident

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with demo data"

    def handle(self, *args, **options):
        # --- Users ---
        admin, _ = User.objects.get_or_create(
            username="admin", defaults={"role": User.Role.ADMIN, "is_staff": True, "is_superuser": True}
        )
        admin.set_password("admin123")
        admin.save()

        staff1, _ = User.objects.get_or_create(username="nurse_zhang", defaults={"role": User.Role.STAFF})
        staff1.set_password("staff123")
        staff1.save()

        staff2, _ = User.objects.get_or_create(username="doctor_li", defaults={"role": User.Role.STAFF})
        staff2.set_password("staff123")
        staff2.save()

        self.stdout.write(self.style.SUCCESS("Users seeded."))

        # --- Training modules (3) ---
        m1, _ = Module.objects.get_or_create(
            title="Hand Hygiene Essentials",
            defaults={"description": "WHO Five Moments for Hand Hygiene", "content": "Hand hygiene content...", "pass_mark": 60},
        )
        m2, _ = Module.objects.get_or_create(
            title="Infection Control Basics",
            defaults={"description": "Standard precautions and infection prevention", "content": "Infection control content...", "pass_mark": 70},
        )
        m3, _ = Module.objects.get_or_create(
            title="PPE Donning and Doffing",
            defaults={"description": "Correct sequence for PPE use", "content": "PPE content...", "pass_mark": 70},
        )
        for m in [m1, m2, m3]:
            for i in range(3):
                Question.objects.get_or_create(
                    module=m, text=f"Sample question {i+1} for {m.title}?",
                    defaults={"options": ["Option A", "Option B", "Option C", "Option D"], "correct_index": 0},
                )

        # Enroll both staff
        for staff in [staff1, staff2]:
            Enrollment.objects.get_or_create(user=staff, module=m1, defaults={"status": Enrollment.Status.COMPLETED, "score": 80, "completed_at": timezone.now()})
            Enrollment.objects.get_or_create(user=staff, module=m2, defaults={"status": Enrollment.Status.IN_PROGRESS})
            Enrollment.objects.get_or_create(user=staff, module=m3)

        self.stdout.write(self.style.SUCCESS("Training data seeded."))

        # --- Compliance requirements (3) ---
        r1, _ = Requirement.objects.get_or_create(
            title="Hand Hygiene Certification",
            defaults={"description": "Annual hand hygiene competency", "category": "Infection Control", "frequency_days": 365},
        )
        r2, _ = Requirement.objects.get_or_create(
            title="Infection Control Training",
            defaults={"description": "Annual infection prevention training", "category": "Infection Control", "frequency_days": 365},
        )
        r3, _ = Requirement.objects.get_or_create(
            title="Workplace Safety Induction",
            defaults={"description": "Biennial safety induction", "category": "Occupational Safety", "frequency_days": 730},
        )
        now = timezone.now()
        for staff in [staff1, staff2]:
            ComplianceRecord.objects.get_or_create(user=staff, requirement=r1, defaults={"last_completed_at": now - timedelta(days=30), "due_at": now + timedelta(days=335)})
            ComplianceRecord.objects.get_or_create(user=staff, requirement=r2, defaults={"last_completed_at": now - timedelta(days=370), "due_at": now - timedelta(days=5)})
            ComplianceRecord.objects.get_or_create(user=staff, requirement=r3, defaults={"last_completed_at": now - timedelta(days=100), "due_at": now + timedelta(days=630)})

        self.stdout.write(self.style.SUCCESS("Compliance data seeded."))

        # --- Incidents (2) ---
        Incident.objects.get_or_create(
            title="Patient fall in Ward 3", reporter=staff1,
            defaults={"description": "Patient slipped near bathroom. No injury.", "location": "Ward 3", "severity": Incident.Severity.LOW},
        )
        Incident.objects.get_or_create(
            title="Needlestick injury in ER", reporter=staff2,
            defaults={"description": "Nurse stuck while recapping needle. PEP initiated.", "location": "Emergency Room", "severity": Incident.Severity.HIGH},
        )

        self.stdout.write(self.style.SUCCESS("Incidents seeded."))
```

- [ ] **Step 4: Register the seed app and run**

Add `"seed"` to `INSTALLED_APPS` in `config/settings.py`. Then:

```bash
cd healthcare_platform/backend && python manage.py seed_data
```

Expected: `Users seeded. Training data seeded. Compliance data seeded. Incidents seeded.`

- [ ] **Step 5: Commit**

```bash
git add healthcare_platform/backend/seed/
git commit -m "feat: add seed data (3 modules, 3 requirements, 2 incidents, 5 docs)"
```

---

## Phase 2: REST APIs

### Task 2.1: Create accounts serializers, views, and URLs (JWT auth)

**Files:**
- Create: `healthcare_platform/backend/accounts/serializers.py`
- Create: `healthcare_platform/backend/accounts/views.py`
- Create: `healthcare_platform/backend/accounts/urls.py`

- [ ] **Step 1: Create accounts/serializers.py**

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")
```

- [ ] **Step 2: Create accounts/views.py**

```python
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer


class MeView(APIView):
    """Return the currently authenticated user's profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class StaffListView(generics.ListAPIView):
    """Admin: list all staff members."""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        User = self.serializer_class.Meta.model
        return User.objects.filter(role=User.Role.STAFF)
```

- [ ] **Step 3: Create accounts/urls.py**

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.MeView.as_view(), name="me"),
]
```

- [ ] **Step 4: Create Django admin superuser (for manual admin tasks)**

```bash
cd healthcare_platform/backend && python manage.py createsuperuser --username admin --email admin@example.com
# Enter password: admin123
```

- [ ] **Step 5: Test JWT login**

```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"username":"nurse_zhang","password":"staff123"}'
```

Expected: returns `{"access": "...", "refresh": "..."}`

- [ ] **Step 6: Commit**

```bash
git add healthcare_platform/backend/accounts/
git commit -m "feat: add accounts API (JWT login, me endpoint)"
```

### Task 2.2: Create training serializers, views, and URLs

**Files:**
- Create: `healthcare_platform/backend/training/serializers.py`
- Create: `healthcare_platform/backend/training/views.py`
- Create: `healthcare_platform/backend/training/urls.py`

- [ ] **Step 1: Create training/serializers.py**

```python
from rest_framework import serializers
from .models import Module, Question, Enrollment


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "text", "options", "correct_index")


class QuestionWithoutAnswerSerializer(serializers.ModelSerializer):
    """For staff: don't expose correct_index until after submission."""
    class Meta:
        model = Question
        fields = ("id", "text", "options")


class ModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ("id", "title", "description", "pass_mark")


class ModuleDetailSerializer(serializers.ModelSerializer):
    questions = QuestionWithoutAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ("id", "title", "description", "content", "pass_mark", "questions")


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("id", "user", "module", "status", "score", "completed_at")
        read_only_fields = ("user",)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class QuizSubmissionSerializer(serializers.Serializer):
    """Expects list of {question_id: int, selected_index: int}."""
    answers = serializers.ListField(child=serializers.DictField())
```

- [ ] **Step 2: Create training/views.py**

```python
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Module, Enrollment, Question
from .serializers import (
    ModuleListSerializer, ModuleDetailSerializer, EnrollmentSerializer,
    QuizSubmissionSerializer, QuestionSerializer,
)


class ModuleListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Module.objects.all()
    serializer_class = ModuleListSerializer


class ModuleDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Module.objects.prefetch_related("questions")
    serializer_class = ModuleDetailSerializer


class EnrollmentView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related("module")

    def perform_create(self, serializer):
        enrollment = serializer.save(user=self.request.user, status=Enrollment.Status.IN_PROGRESS)
        return enrollment


class SubmitQuizView(APIView):
    """Grade a quiz submission: compare selected answers to correct answers."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, module_id):
        serializer = QuizSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = {a["question_id"]: a["selected_index"] for a in serializer.validated_data["answers"]}

        questions = Question.objects.filter(module_id=module_id)
        correct = sum(1 for q in questions if answers.get(q.id) == q.correct_index)
        total = questions.count()
        score = int(correct / total * 100) if total else 0
        passed = score >= questions.first().module.pass_mark if total else False

        enrollment = Enrollment.objects.get(user=request.user, module_id=module_id)
        enrollment.score = score
        enrollment.status = Enrollment.Status.COMPLETED if passed else Enrollment.Status.IN_PROGRESS
        if passed:
            enrollment.completed_at = timezone.now()
        enrollment.save()

        return Response({"score": score, "total": total, "correct": correct, "passed": passed})
```

- [ ] **Step 3: Create training/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ModuleListView.as_view(), name="module-list"),
    path("<int:pk>/", views.ModuleDetailView.as_view(), name="module-detail"),
    path("enrollments/", views.EnrollmentView.as_view(), name="enrollments"),
    path("<int:module_id>/submit/", views.SubmitQuizView.as_view(), name="submit-quiz"),
]
```

- [ ] **Step 4: Test**

```bash
python manage.py runserver &
# GET /api/training/ - list 3 modules
# GET /api/training/1/ - module detail with questions
# POST /api/training/enrollments/ -- enroll
# POST /api/training/1/submit/ -- submit quiz answers
```

- [ ] **Step 5: Commit**

```bash
git add healthcare_platform/backend/training/serializers.py healthcare_platform/backend/training/views.py healthcare_platform/backend/training/urls.py
git commit -m "feat: add training CRUD + quiz submission API"
```

### Task 2.3: Create compliance serializers, views, and URLs

**Files:**
- Create: `healthcare_platform/backend/compliance/serializers.py`
- Create: `healthcare_platform/backend/compliance/views.py`
- Create: `healthcare_platform/backend/compliance/urls.py`

- [ ] **Step 1: Create compliance/serializers.py**

```python
from rest_framework import serializers
from .models import Requirement, ComplianceRecord


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"


class ComplianceRecordSerializer(serializers.ModelSerializer):
    requirement_title = serializers.CharField(source="requirement.title", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceRecord
        fields = ("id", "requirement", "requirement_title", "last_completed_at", "due_at", "status")

    def get_status(self, obj):
        return obj.compute_status()
```

- [ ] **Step 2: Create compliance/views.py**

```python
from rest_framework import generics, permissions
from .models import ComplianceRecord
from .serializers import ComplianceRecordSerializer


class ComplianceListView(generics.ListAPIView):
    """Staff sees their own compliance; admin sees all."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ComplianceRecordSerializer

    def get_queryset(self):
        qs = ComplianceRecord.objects.select_related("requirement", "user")
        if self.request.user.role == "ADMIN":
            return qs
        return qs.filter(user=self.request.user)
```

- [ ] **Step 3: Create compliance/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ComplianceListView.as_view(), name="compliance-list"),
]
```

- [ ] **Step 4: Commit**

```bash
git add healthcare_platform/backend/compliance/
git commit -m "feat: add compliance list API with on-read status computation"
```

### Task 2.4: Create incidents serializers, views, and URLs

**Files:**
- Create: `healthcare_platform/backend/incidents/serializers.py`
- Create: `healthcare_platform/backend/incidents/views.py`
- Create: `healthcare_platform/backend/incidents/urls.py`

- [ ] **Step 1: Create incidents/serializers.py**

```python
from rest_framework import serializers
from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source="reporter.username", read_only=True)

    class Meta:
        model = Incident
        fields = ("id", "title", "description", "location", "severity",
                  "status", "reporter", "reporter_name", "created_at", "resolved_at")
        read_only_fields = ("reporter", "status", "created_at", "resolved_at")

    def create(self, validated_data):
        validated_data["reporter"] = self.context["request"].user
        return super().create(validated_data)
```

- [ ] **Step 2: Create incidents/views.py**

```python
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Incident
from .serializers import IncidentSerializer


class IncidentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncidentSerializer

    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return Incident.objects.select_related("reporter").all()
        return Incident.objects.filter(reporter=self.request.user)


class IncidentUpdateView(generics.UpdateAPIView):
    """Admin updates incident status."""
    permission_classes = [permissions.IsAdminUser]
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def perform_update(self, serializer):
        if serializer.validated_data.get("status") == Incident.Status.RESOLVED:
            serializer.save(resolved_at=timezone.now())
        else:
            serializer.save()
```

- [ ] **Step 3: Create incidents/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IncidentListCreateView.as_view(), name="incident-list"),
    path("<int:pk>/", views.IncidentUpdateView.as_view(), name="incident-update"),
]
```

- [ ] **Step 4: Commit**

```bash
git add healthcare_platform/backend/incidents/
git commit -m "feat: add incidents API (staff create+list, admin update status)"
```

### Task 2.5: Create chatbot ask endpoint (without RAG — returns fallback first)

**Files:**
- Create: `healthcare_platform/backend/chatbot/serializers.py`
- Create: `healthcare_platform/backend/chatbot/views.py`
- Create: `healthcare_platform/backend/chatbot/urls.py`
- Create: `healthcare_platform/backend/chatbot/rag.py`

- [ ] **Step 1: Create chatbot/serializers.py** — ask request/response serializers

```python
from rest_framework import serializers


class AskRequestSerializer(serializers.Serializer):
    question = serializers.CharField(min_length=1, max_length=1000)


class AskResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    sources = serializers.ListField(child=serializers.CharField())
```

- [ ] **Step 2: Create chatbot/rag.py** — RAG pipeline stub (Phase 3 fills this in)

```python
"""
RAG pipeline for the healthcare compliance chatbot.
Phase 3 will implement embedding + retrieval + OpenRouter calls.
For now, this stub returns a fallback message.
"""

from .models import Chunk


def retrieve_chunks(question: str, top_k: int = 5) -> list[dict]:
    """Stub: returns empty list until pgvector is populated. Phase 3 implements this."""
    return []


def generate_answer(question: str, chunks: list[dict]) -> tuple[str, list[str]]:
    """Stub: returns fallback. Phase 3 wires OpenRouter."""
    return (
        "I'm still being trained on the compliance documents. Please check back later.",
        [],
    )
```

- [ ] **Step 3: Create chatbot/views.py**

```python
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AskRequestSerializer
from .rag import retrieve_chunks, generate_answer


class AskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data["question"]

        chunks = retrieve_chunks(question)
        answer, sources = generate_answer(question, chunks)

        return Response({"answer": answer, "sources": sources})
```

- [ ] **Step 4: Create chatbot/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("ask/", views.AskView.as_view(), name="chatbot-ask"),
]
```

- [ ] **Step 5: Test stub**

```bash
curl -X POST http://localhost:8000/api/chatbot/ask/ -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"question":"How do I wash my hands?"}'
```

Expected: `{"answer":"I'm still being trained on the compliance documents...","sources":[]}`

- [ ] **Step 6: Commit**

```bash
git add healthcare_platform/backend/chatbot/serializers.py healthcare_platform/backend/chatbot/views.py healthcare_platform/backend/chatbot/urls.py healthcare_platform/backend/chatbot/rag.py
git commit -m "feat: add chatbot ask endpoint (stub, returns fallback)"
```

---

## Phase 3: RAG Ingestion Pipeline

### Task 3.1: Implement document ingestion (chunking + embedding + storage)

**Files:**
- Modify: `healthcare_platform/backend/chatbot/rag.py`
- Create: `healthcare_platform/backend/chatbot/management/commands/ingest_docs.py`

- [ ] **Step 1: Add ingestion functions to chatbot/rag.py**

Replace the entire contents of `healthcare_platform/backend/chatbot/rag.py`:

```python
"""
RAG pipeline for the healthcare compliance chatbot.
Uses fastembed (BAAI/bge-small-en, 384-dim) for embeddings,
pgvector for similarity search, and OpenRouter's Llama 4 Maverick for answer generation.
"""

import os
from typing import Optional

from pgvector.django import L2Distance

from .models import Document, Chunk

# Embedding model — loaded once at module level
_embedder = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        from fastembed import TextEmbedding
        _embedder = TextEmbedding(model_name="BAAI/bge-small-en")
    return _embedder


def embed_text(text: str) -> list[float]:
    """Generate a 384-dim embedding for a single text string."""
    embedder = _get_embedder()
    result = next(embedder.embed([text]))
    return result.tolist()


# ----- Chunking -----

def _split_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Split plain text into overlapping word-level chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# ----- Ingestion (offline) -----

def ingest_document(document: Document, text: str) -> int:
    """Split a document into chunks, embed each, and store. Returns number of chunks created."""
    Chunk.objects.filter(document=document).delete()  # re-ingest cleanly
    chunk_texts = _split_text(text)
    chunks = []
    for i, ct in enumerate(chunk_texts):
        emb = embed_text(ct)
        chunks.append(Chunk(document=document, content=ct, chunk_index=i, embedding=emb))
    Chunk.objects.bulk_create(chunks)
    return len(chunks)


# ----- Retrieval -----

def retrieve_chunks(question: str, top_k: int = 5) -> list[dict]:
    """Embed the question, find top-k most similar chunks via pgvector L2 distance."""
    try:
        q_embedding = embed_text(question)
    except Exception:
        return []  # graceful fallback if embedding fails

    chunks = (
        Chunk.objects.annotate(distance=L2Distance("embedding", q_embedding))
        .select_related("document")
        .order_by("distance")
    )[:top_k]

    return [
        {"content": c.content, "document_title": c.document.title}
        for c in chunks
    ]


# ----- Answer Generation (OpenRouter / Llama 4 Maverick) -----

SYSTEM_PROMPT = (
    "You are a healthcare compliance and safety expert. "
    "Use ONLY the context provided below to answer the user's question. "
    "If the context does not contain enough information, say 'I don't have enough information to answer that.' "
    "Cite the document titles you used in your answer."
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_answer(question: str, chunks: list[dict]) -> tuple[str, list[str]]:
    """Build a RAG prompt and call OpenRouter. Returns (answer, source_titles)."""
    if not chunks:
        return ("I couldn't find any relevant compliance documents for your question.", [])

    context = "\n\n".join(
        f"[{c['document_title']}]\n{c['content']}" for c in chunks
    )
    user_message = f"Context:\n\n{context}\n\nQuestion: {question}"

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        # Fallback: return raw chunks
        sources = list({c["document_title"] for c in chunks})
        fallback = "\n\n".join(f"[{c['document_title']}] {c['content'][:400]}" for c in chunks[:3])
        return (
            f"(OpenRouter API key not configured. Returning raw results.)\n\n{fallback}",
            sources,
        )

    import httpx
    try:
        resp = httpx.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-4-maverick:free",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": 500,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        body = resp.json()
        answer = body["choices"][0]["message"]["content"]
    except Exception as e:
        # Fallback: return raw chunks
        sources = list({c["document_title"] for c in chunks})
        fallback = "\n\n".join(f"[{c['document_title']}] {c['content'][:400]}" for c in chunks[:3])
        return (
            f"(LLM request failed: {e})\n\nRelevant document excerpts:\n\n{fallback}",
            sources,
        )

    sources = list({c["document_title"] for c in chunks})
    return answer, sources
```

- [ ] **Step 2: Create management command to ingest seed docs**

Create `healthcare_platform/backend/chatbot/management/__init__.py`:

```python
```

Create `healthcare_platform/backend/chatbot/management/commands/__init__.py`:

```python
```

Create `healthcare_platform/backend/chatbot/management/commands/ingest_docs.py`:

```python
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chatbot.models import Document
from chatbot.rag import ingest_document

User = get_user_model()
SEED_DOCS_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "seed" / "docs"

DOC_TITLES = {
    "hand_hygiene.txt": ("Hand Hygiene Protocol", "WHO Five Moments for Hand Hygiene"),
    "infection_control.txt": ("Infection Control and Prevention", "CDC Standard Precautions"),
    "incident_protocol.txt": ("Incident Reporting Protocol", "Internal Safety Policy"),
    "ppe_guidelines.txt": ("PPE Donning and Doffing Guidelines", "OSHA PPE Standard"),
    "workplace_safety.txt": ("Workplace Health and Safety", "Facility Safety Manual"),
}


class Command(BaseCommand):
    help = "Ingest seed healthcare compliance documents into the RAG knowledge base"

    def handle(self, *args, **options):
        admin = User.objects.filter(role=User.Role.ADMIN).first()
        total_chunks = 0

        for filename, (title, source) in DOC_TITLES.items():
            filepath = SEED_DOCS_DIR / filename
            if not filepath.exists():
                self.stdout.write(self.style.WARNING(f"Skipping {filename} — file not found"))
                continue

            text = filepath.read_text(encoding="utf-8")
            doc, created = Document.objects.get_or_create(
                title=title, defaults={"source": source, "uploaded_by": admin},
            )
            n = ingest_document(doc, text)
            total_chunks += n
            action = "Created and ingested" if created else "Re-ingested"
            self.stdout.write(self.style.SUCCESS(f"{action} '{title}' → {n} chunks"))

        self.stdout.write(self.style.SUCCESS(f"Done. Total chunks indexed: {total_chunks}"))
```

- [ ] **Step 3: Run ingestion**

```bash
cd healthcare_platform/backend && python manage.py ingest_docs
```

Expected: each document ingested with chunks, total printed.

- [ ] **Step 4: Test the chatbot ask endpoint now returns real results**

```bash
curl -X POST http://localhost:8000/api/chatbot/ask/ -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"question":"When should I wash my hands?"}'
```

Expected: returns answer with sources from the ingested documents (without OPENROUTER_API_KEY set, returns fallback + raw chunks; with the key set, returns LLM answer).

- [ ] **Step 5: Commit**

```bash
git add healthcare_platform/backend/chatbot/
git commit -m "feat: implement RAG pipeline (chunking, embedding, pgvector retrieval, OpenRouter)"
```

---

## Phase 4: React Frontend

### Task 4.1: Scaffold Vite React project

**Files:**
- Create: `healthcare_platform/frontend/package.json`
- Create: `healthcare_platform/frontend/vite.config.js`
- Create: `healthcare_platform/frontend/index.html`
- Create: `healthcare_platform/frontend/src/main.jsx`
- Create: `healthcare_platform/frontend/src/App.jsx`
- Create: `healthcare_platform/frontend/src/styles/global.css`

- [ ] **Step 1: Create package.json**

Create `healthcare_platform/frontend/package.json`:

```json
{
  "name": "healthcare-platform",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0",
    "axios": "^1.7.9"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.0"
  }
}
```

- [ ] **Step 2: Create vite.config.js**

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
```

- [ ] **Step 3: Create index.html**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Healthcare Compliance Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

- [ ] **Step 4: Create main.jsx**

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./auth/AuthContext";
import "./styles/global.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

- [ ] **Step 5: Create App.jsx (shell with routes)**

```jsx
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import LoginPage from "./auth/LoginPage";
import ProtectedRoute from "./auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import TrainingList from "./pages/TrainingList";
import TrainingDetail from "./pages/TrainingDetail";
import ComplianceList from "./pages/ComplianceList";
import IncidentList from "./pages/IncidentList";
import IncidentForm from "./pages/IncidentForm";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/training" element={<TrainingList />} />
        <Route path="/training/:id" element={<TrainingDetail />} />
        <Route path="/compliance" element={<ComplianceList />} />
        <Route path="/incidents" element={<IncidentList />} />
        <Route path="/incidents/new" element={<IncidentForm />} />
      </Route>
    </Routes>
  );
}
```

- [ ] **Step 6: Create global.css**

Create `healthcare_platform/frontend/src/styles/global.css`:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; }
a { color: #1a73e8; text-decoration: none; }
button { cursor: pointer; }
```

- [ ] **Step 7: Install and verify dev server**

```bash
cd healthcare_platform/frontend && npm install && npm run dev
```

Open http://localhost:5173 — should see a blank page (no routes matched yet = blank). No errors in console.

- [ ] **Step 8: Commit**

```bash
git add healthcare_platform/frontend/
git commit -m "feat: scaffold Vite + React project with router"
```

### Task 4.2: Create API client and auth system

**Files:**
- Create: `healthcare_platform/frontend/src/api/client.js`
- Create: `healthcare_platform/frontend/src/auth/AuthContext.jsx`
- Create: `healthcare_platform/frontend/src/auth/LoginPage.jsx`
- Create: `healthcare_platform/frontend/src/auth/ProtectedRoute.jsx`

- [ ] **Step 1: Create api/client.js**

```js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = axios.create({ baseURL: `${API_BASE}/api` });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default client;
```

- [ ] **Step 2: Create AuthContext.jsx**

```jsx
import { createContext, useContext, useState, useEffect } from "react";
import client from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (username, password) => {
    const res = await client.post("/auth/login/", { username, password });
    localStorage.setItem("access_token", res.data.access);
    localStorage.setItem("refresh_token", res.data.refresh);
    await fetchUser();
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  };

  const fetchUser = async () => {
    try {
      const res = await client.get("/auth/me/");
      setUser(res.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (localStorage.getItem("access_token")) fetchUser(); else setLoading(false); }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

- [ ] **Step 3: Create LoginPage.jsx**

```jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(username, password);
      navigate("/dashboard");
    } catch {
      setError("Login failed. Check your credentials.");
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", background: "#e8f0fe" }}>
      <form onSubmit={handleSubmit} style={{ background: "#fff", padding: 40, borderRadius: 8, boxShadow: "0 2px 8px rgba(0,0,0,0.1)", width: 360 }}>
        <h1 style={{ marginBottom: 24, textAlign: "center" }}>Healthcare Compliance</h1>
        {error && <p style={{ color: "red", marginBottom: 12 }}>{error}</p>}
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)}
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 12, border: "1px solid #ddd", borderRadius: 4 }} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 16, border: "1px solid #ddd", borderRadius: 4 }} />
        <button type="submit" style={{ width: "100%", padding: 12, background: "#1a73e8", color: "#fff", border: "none", borderRadius: 4, fontSize: 16 }}>
          Sign In
        </button>
      </form>
    </div>
  );
}
```

- [ ] **Step 4: Create ProtectedRoute.jsx**

```jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <p style={{ padding: 40 }}>Loading...</p>;
  if (!user) return <Navigate to="/login" />;
  return children;
}
```

- [ ] **Step 5: Commit**

```bash
git add healthcare_platform/frontend/src/api/ healthcare_platform/frontend/src/auth/
git commit -m "feat: add API client with JWT interceptor, auth context, and login page"
```

### Task 4.3: Create Layout with sidebar navigation

**Files:**
- Create: `healthcare_platform/frontend/src/components/Layout.jsx`

- [ ] **Step 1: Create Layout.jsx**

```jsx
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import ChatWidget from "./ChatWidget";

const navItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/training", label: "Training" },
  { to: "/compliance", label: "Compliance" },
  { to: "/incidents", label: "Incidents" },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const linkStyle = ({ isActive }) => ({
    display: "block", padding: "10px 16px", color: isActive ? "#fff" : "#cbd5e1",
    background: isActive ? "#1e293b" : "transparent", borderRadius: 4, marginBottom: 4,
  });

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside style={{ width: 220, background: "#0f172a", color: "#fff", padding: "20px 12px", display: "flex", flexDirection: "column" }}>
        <h2 style={{ fontSize: 16, marginBottom: 24, paddingLeft: 12 }}>HC Platform</h2>
        <nav style={{ flex: 1 }}>
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} style={linkStyle}>{item.label}</NavLink>
          ))}
        </nav>
        <div style={{ borderTop: "1px solid #334155", paddingTop: 12 }}>
          <p style={{ fontSize: 13, color: "#94a3b8", paddingLeft: 12 }}>{user?.username} ({user?.role})</p>
          <button onClick={handleLogout} style={{ width: "100%", marginTop: 8, padding: 8, background: "#334155", color: "#fff", border: "none", borderRadius: 4 }}>Logout</button>
        </div>
      </aside>
      <main style={{ flex: 1, padding: 32 }}>
        <Outlet />
      </main>
      <ChatWidget />
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add healthcare_platform/frontend/src/components/Layout.jsx
git commit -m "feat: add sidebar layout with navigation and logout"
```

### Task 4.4: Create Dashboard page

**Files:**
- Create: `healthcare_platform/frontend/src/pages/Dashboard.jsx`

- [ ] **Step 1: Create Dashboard.jsx**

```jsx
import { useState, useEffect } from "react";
import client from "../api/client";

export default function Dashboard() {
  const [stats, setStats] = useState({ modules: 0, compliant: 0, totalReq: 0, incidents: 0 });

  useEffect(() => {
    Promise.all([
      client.get("/training/"),
      client.get("/compliance/"),
      client.get("/incidents/"),
    ]).then(([training, compliance, incidents]) => {
      const records = compliance.data || [];
      setStats({
        modules: training.data.length,
        compliant: records.filter((r) => r.status === "COMPLIANT").length,
        totalReq: records.length,
        incidents: incidents.data.length,
      });
    }).catch(console.error);
  }, []);

  const cards = [
    { label: "Training Modules", value: stats.modules, color: "#1a73e8" },
    { label: "Compliant", value: `${stats.compliant}/${stats.totalReq}`, color: "#0d9488" },
    { label: "Reported Incidents", value: stats.incidents, color: "#d97706" },
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>Dashboard</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16 }}>
        {cards.map((c) => (
          <div key={c.label} style={{ background: "#fff", padding: 24, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", borderLeft: `4px solid ${c.color}` }}>
            <p style={{ fontSize: 14, color: "#64748b", marginBottom: 8 }}>{c.label}</p>
            <p style={{ fontSize: 28, fontWeight: 700 }}>{c.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add healthcare_platform/frontend/src/pages/Dashboard.jsx
git commit -m "feat: add dashboard with summary cards"
```

### Task 4.5: Create Training pages

**Files:**
- Create: `healthcare_platform/frontend/src/pages/TrainingList.jsx`
- Create: `healthcare_platform/frontend/src/pages/TrainingDetail.jsx`

- [ ] **Step 1: Create TrainingList.jsx**

```jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import client from "../api/client";

export default function TrainingList() {
  const [modules, setModules] = useState([]);

  useEffect(() => {
    client.get("/training/").then((r) => setModules(r.data)).catch(console.error);
  }, []);

  return (
    <div>
      <h1>Training Modules</h1>
      <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
        {modules.map((m) => (
          <Link key={m.id} to={`/training/${m.id}`}
            style={{ display: "block", background: "#fff", padding: 16, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)" }}>
            <strong>{m.title}</strong>
            <p style={{ color: "#64748b", marginTop: 4 }}>{m.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create TrainingDetail.jsx**

```jsx
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import client from "../api/client";

export default function TrainingDetail() {
  const { id } = useParams();
  const [module, setModule] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    client.get(`/training/${id}/`).then((r) => setModule(r.data)).catch(console.error);
  }, [id]);

  const handleSubmit = async () => {
    const payload = { answers: Object.entries(answers).map(([qid, idx]) => ({ question_id: Number(qid), selected_index: idx })) };
    const res = await client.post(`/training/${id}/submit/`, payload);
    setResult(res.data);
  };

  if (!module) return <p>Loading...</p>;

  return (
    <div>
      <h1>{module.title}</h1>
      <p style={{ color: "#64748b", marginBottom: 24 }}>{module.description}</p>
      <div style={{ background: "#f8fafc", padding: 16, borderRadius: 8, marginBottom: 24 }}>{module.content}</div>

      {!result && module.questions.map((q) => (
        <div key={q.id} style={{ background: "#fff", padding: 16, borderRadius: 8, marginBottom: 12, boxShadow: "0 1px 4px rgba(0,0,0,0.08)" }}>
          <p style={{ fontWeight: 600, marginBottom: 8 }}>{q.text}</p>
          {q.options.map((opt, i) => (
            <label key={i} style={{ display: "block", marginBottom: 4 }}>
              <input type="radio" name={`q-${q.id}`} value={i} checked={answers[q.id] === i} onChange={() => setAnswers({ ...answers, [q.id]: i })} />
              {" "}{opt}
            </label>
          ))}
        </div>
      ))}
      {result && (
        <div style={{ background: result.passed ? "#d1fae5" : "#fee2e2", padding: 16, borderRadius: 8, marginBottom: 24 }}>
          <p style={{ fontSize: 18, fontWeight: 700 }}>Score: {result.score}% ({result.correct}/{result.total}) — {result.passed ? "PASSED" : "FAILED"}</p>
        </div>
      )}
      {!result && (
        <button onClick={handleSubmit} style={{ padding: "12px 32px", background: "#1a73e8", color: "#fff", border: "none", borderRadius: 6, fontSize: 16 }}>
          Submit Quiz
        </button>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/frontend/src/pages/TrainingList.jsx healthcare_platform/frontend/src/pages/TrainingDetail.jsx
git commit -m "feat: add training list and quiz pages"
```

### Task 4.6: Create Compliance page

**Files:**
- Create: `healthcare_platform/frontend/src/pages/ComplianceList.jsx`

- [ ] **Step 1: Create ComplianceList.jsx**

```jsx
import { useState, useEffect } from "react";
import client from "../api/client";

const statusColor = { COMPLIANT: "#0d9488", DUE: "#d97706", OVERDUE: "#dc2626" };

export default function ComplianceList() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    client.get("/compliance/").then((r) => setRecords(r.data)).catch(console.error);
  }, []);

  return (
    <div>
      <h1>Compliance Status</h1>
      <div style={{ marginTop: 16 }}>
        {records.map((r) => (
          <div key={r.id} style={{ background: "#fff", padding: 16, borderRadius: 8, marginBottom: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong>{r.requirement_title}</strong>
              <p style={{ color: "#64748b", fontSize: 14 }}>Last: {r.last_completed_at ? new Date(r.last_completed_at).toLocaleDateString() : "N/A"}  |  Due: {r.due_at ? new Date(r.due_at).toLocaleDateString() : "N/A"}</p>
            </div>
            <span style={{ padding: "4px 12px", borderRadius: 12, color: "#fff", background: statusColor[r.status] || "#64748b", fontSize: 13, fontWeight: 600 }}>
              {r.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add healthcare_platform/frontend/src/pages/ComplianceList.jsx
git commit -m "feat: add compliance status page"
```

### Task 4.7: Create Incidents pages

**Files:**
- Create: `healthcare_platform/frontend/src/pages/IncidentList.jsx`
- Create: `healthcare_platform/frontend/src/pages/IncidentForm.jsx`

- [ ] **Step 1: Create IncidentList.jsx**

```jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import client from "../api/client";
import { useAuth } from "../auth/AuthContext";

const statusColors = { SUBMITTED: "#6366f1", UNDER_REVIEW: "#d97706", RESOLVED: "#0d9488" };

export default function IncidentList() {
  const [incidents, setIncidents] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    client.get("/incidents/").then((r) => setIncidents(r.data)).catch(console.error);
  }, []);

  const markResolved = async (id) => {
    await client.patch(`/incidents/${id}/`, { status: "RESOLVED" });
    setIncidents((prev) => prev.map((i) => (i.id === id ? { ...i, status: "RESOLVED" } : i)));
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1>Incidents</h1>
        {user?.role === "STAFF" && <Link to="/incidents/new" style={{ padding: "10px 20px", background: "#1a73e8", color: "#fff", borderRadius: 6 }}>+ Report Incident</Link>}
      </div>
      {incidents.map((i) => (
        <div key={i.id} style={{ background: "#fff", padding: 16, borderRadius: 8, marginBottom: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)" }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <strong>{i.title}</strong> <span style={{ fontSize: 12, color: "#64748b" }}>— {i.location}</span>
              <p style={{ color: "#64748b", marginTop: 4 }}>{i.description}</p>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{ padding: "4px 12px", borderRadius: 12, color: "#fff", background: statusColors[i.status], fontSize: 12 }}>{i.status}</span>
              <p style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>{i.severity}</p>
            </div>
          </div>
          {user?.role === "ADMIN" && i.status !== "RESOLVED" && (
            <button onClick={() => markResolved(i.id)} style={{ marginTop: 8, padding: "6px 16px", background: "#0d9488", color: "#fff", border: "none", borderRadius: 4 }}>
              Mark Resolved
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create IncidentForm.jsx**

```jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function IncidentForm() {
  const [form, setForm] = useState({ title: "", description: "", location: "", severity: "LOW" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await client.post("/incidents/", form);
    navigate("/incidents");
  };

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  return (
    <div>
      <h1>Report Incident</h1>
      <form onSubmit={handleSubmit} style={{ maxWidth: 600, marginTop: 16 }}>
        <input placeholder="Title" value={form.title} onChange={set("title")} required
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 12, border: "1px solid #ddd", borderRadius: 4 }} />
        <textarea placeholder="Description" value={form.description} onChange={set("description")} rows={4} required
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 12, border: "1px solid #ddd", borderRadius: 4 }} />
        <input placeholder="Location" value={form.location} onChange={set("location")} required
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 12, border: "1px solid #ddd", borderRadius: 4 }} />
        <select value={form.severity} onChange={set("severity")}
          style={{ display: "block", width: "100%", padding: 10, marginBottom: 16, border: "1px solid #ddd", borderRadius: 4 }}>
          <option value="LOW">Low</option><option value="MEDIUM">Medium</option><option value="HIGH">High</option><option value="CRITICAL">Critical</option>
        </select>
        <button type="submit" style={{ padding: "12px 32px", background: "#1a73e8", color: "#fff", border: "none", borderRadius: 6, fontSize: 16 }}>Submit Report</button>
      </form>
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/frontend/src/pages/IncidentList.jsx healthcare_platform/frontend/src/pages/IncidentForm.jsx
git commit -m "feat: add incident list and report form pages"
```

### Task 4.8: Create ChatWidget component

**Files:**
- Create: `healthcare_platform/frontend/src/components/ChatWidget.jsx`

- [ ] **Step 1: Create ChatWidget.jsx**

```jsx
import { useState } from "react";
import client from "../api/client";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question.trim()) return;
    const q = question;
    setMessages((m) => [...m, { role: "user", content: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await client.post("/chatbot/ask/", { question: q });
      setMessages((m) => [...m, { role: "assistant", content: res.data.answer, sources: res.data.sources }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "Sorry, something went wrong." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {!open && (
        <button onClick={() => setOpen(true)}
          style={{ position: "fixed", bottom: 24, right: 24, width: 56, height: 56, borderRadius: 28, background: "#1a73e8", color: "#fff", border: "none", fontSize: 24, boxShadow: "0 4px 12px rgba(0,0,0,0.2)" }}>
          💬
        </button>
      )}
      {open && (
        <div style={{ position: "fixed", bottom: 24, right: 24, width: 380, height: 500, background: "#fff", borderRadius: 12, boxShadow: "0 4px 24px rgba(0,0,0,0.15)", display: "flex", flexDirection: "column" }}>
          <div style={{ padding: "12px 16px", background: "#1a73e8", color: "#fff", borderRadius: "12px 12px 0 0", display: "flex", justifyContent: "space-between" }}>
            <span style={{ fontWeight: 600 }}>Compliance Assistant</span>
            <button onClick={() => setOpen(false)} style={{ background: "none", border: "none", color: "#fff", fontSize: 18 }}>✕</button>
          </div>
          <div style={{ flex: 1, overflow: "auto", padding: 12 }}>
            {messages.map((m, i) => (
              <div key={i} style={{ marginBottom: 12, textAlign: m.role === "user" ? "right" : "left" }}>
                <div style={{ display: "inline-block", padding: "8px 12px", borderRadius: 8, background: m.role === "user" ? "#e8f0fe" : "#f1f5f9", maxWidth: "85%", whiteSpace: "pre-wrap", fontSize: 14 }}>
                  {m.content}
                </div>
                {m.sources?.length > 0 && (
                  <p style={{ fontSize: 11, color: "#94a3b8", marginTop: 2 }}>Sources: {m.sources.join(", ")}</p>
                )}
              </div>
            ))}
            {loading && <p style={{ fontSize: 13, color: "#94a3b8" }}>Thinking...</p>}
          </div>
          <div style={{ padding: 12, borderTop: "1px solid #e2e8f0", display: "flex", gap: 8 }}>
            <input value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={(e) => e.key === "Enter" && ask()}
              placeholder="Ask a safety question..." style={{ flex: 1, padding: 10, border: "1px solid #ddd", borderRadius: 6 }} />
            <button onClick={ask} disabled={loading} style={{ padding: "10px 16px", background: "#1a73e8", color: "#fff", border: "none", borderRadius: 6 }}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add healthcare_platform/frontend/src/components/ChatWidget.jsx
git commit -m "feat: add floating chatbot widget"
```

### Task 4.9: Full-stack integration test (local)

- [ ] **Step 1: Start backend**

```bash
cd healthcare_platform/backend && python manage.py runserver &
```

- [ ] **Step 2: Start frontend**

```bash
cd healthcare_platform/frontend && npm run dev &
```

- [ ] **Step 3: Walk through full demo flow**

Open http://localhost:5173 → Login as `nurse_zhang` / `staff123` → Dashboard shows cards → Training → select module → take quiz → Compliance → view status → Incidents → submit → Chatbot → ask question → Logout.

- [ ] **Step 4: Fix any CORS/token/API issues found and commit**

```bash
git add -A
git commit -m "fix: integration fixes from full-stack walkthrough"
```

---

## Phase 5: Deploy

### Task 5.1: Prepare backend for Render

**Files:**
- Create: `healthcare_platform/backend/render.yaml`
- Create: `healthcare_platform/backend/.env.example`

- [ ] **Step 1: Create .env.example**

Create `healthcare_platform/backend/.env.example`:

```
SECRET_KEY=your-django-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ORIGINS=https://your-app.vercel.app
OPENROUTER_API_KEY=sk-or-v1-...
ALLOWED_HOSTS=your-backend.onrender.com,localhost
```

- [ ] **Step 2: Create render.yaml**

Create `healthcare_platform/backend/render.yaml`:

```yaml
services:
  - type: web
    name: healthcare-compliance-api
    runtime: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data
    startCommand: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: "healthcare-compliance-api.onrender.com,localhost"
      - key: CORS_ORIGINS
        sync: false
      - key: DATABASE_URL
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
```

- [ ] **Step 3: Commit**

```bash
git add healthcare_platform/backend/.env.example healthcare_platform/backend/render.yaml
git commit -m "feat: add Render deployment config"
```

### Task 5.2: Prepare frontend for Vercel

**Files:**
- Create: `healthcare_platform/frontend/vercel.json`

- [ ] **Step 1: Create vercel.json**

Create `healthcare_platform/frontend/vercel.json`:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

- [ ] **Step 2: Commit**

```bash
git add healthcare_platform/frontend/vercel.json
git commit -m "feat: add Vercel config for SPA routing"
```

### Task 5.3: Full production build and push

- [ ] **Step 1: Build frontend locally to verify**

```bash
cd healthcare_platform/frontend && npm run build
```

Expected: `dist/` directory created, no errors.

- [ ] **Step 2: Final commit and push**

```bash
cd c:/Users/Administrator/Desktop/MSE800
git add healthcare_platform/
git commit -m "feat: complete healthcare compliance platform MVP"
git push origin main
```

- [ ] **Step 3: Deploy to Render**
  1. Go to https://dashboard.render.com → New Web Service
  2. Connect GitHub repo → set root directory to `healthcare_platform/backend`
  3. Set environment variables: `DATABASE_URL`, `CORS_ORIGINS`, `OPENROUTER_API_KEY`
  4. Render auto-builds (`pip install`, `migrate`, `seed_data`) and starts Gunicorn
  5. Verify: `curl https://healthcare-compliance-api.onrender.com/api/auth/login/` works

- [ ] **Step 4: Deploy to Vercel**
  1. Go to https://vercel.com → Import GitHub repo
  2. Set root directory to `healthcare_platform/frontend`
  3. Set environment variable: `VITE_API_URL=https://healthcare-compliance-api.onrender.com`
  4. Vercel auto-deploys on push
  5. Open the Vercel URL → Login → Full demo walkthrough

- [ ] **Step 5: Run ingest_docs on Render (one-time)**

In Render Dashboard → Shell tab for the web service:

```bash
python manage.py ingest_docs
```

Expected: 5 documents ingested, chunks printed, chatbot `/api/chatbot/ask/` now returns real RAG results.

---

**Plan complete.**
