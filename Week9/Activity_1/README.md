# Intelligent Healthcare Compliance & Safety Management System

Group W: Abu Sufian & Xiao Liang

> **Waterfall Project Management Methodology — 7 Weeks, 6 Phases**

![Waterfall Diagram](./Waterfall_Project_Management.drawio)

---

## 1. Requirements Analysis Phase (Week 1)

The objective is to establish **what** the system must do, culminating in an
unalterable Software Requirements Specification (SRS) document.

### 1.1 Regulatory & Compliance Requirements

- Gather **HIPAA** (U.S.) and **GDPR** (EU) compliance needs: patient data
  privacy, consent management, audit trail, breach notification timelines.
- Map each regulatory requirement to a measurable system feature (e.g., "every
  data access event must be logged with timestamp + user ID").

### 1.2 Stakeholder Roles & Permissions

| Role | Responsibilities |
|---|---|
| **Staff (Nurse, Doctor)** | Complete safety training modules, take quizzes, view own compliance status, report incidents, use the RAG chatbot |
| **Admin (Safety Officer)** | Manage training modules & compliance requirements, review incidents, upload knowledge-base documents, view all staff compliance records |

### 1.3 Functional Requirements

Define **10 deliverable business metrics**:
1. Staff can log in with JWT and see their personalised dashboard
2–4. Training: enrol in module → take 3-question quiz → see score/pass status
5–7. Compliance: view status list (COMPLIANT/DUE/OVERDUE), computed on read
8–9. Incidents: staff submit report → admin reviews → admin marks RESOLVED
10. Chatbot: ask a safety question → receive sourced, RAG-generated answer

### 1.4 Non-Functional Requirements

- **Security:** JWT authentication (2-hour expiry), role-based route protection,
  CORS whitelist, HTTPS on all deployed endpoints
- **Responsiveness:** React SPA with responsive layout (desktop, tablet, mobile)
- **Performance:** API response < 500ms (excluding LLM calls), LLM response < 5s
- **Availability:** Render free-tier auto-wake; frontend warm-up request + retry

### Phase Deliverables

- *Software Requirements Specification (SRS) Document*
- *Stakeholder Role & Permission Matrix*

---

## 2. System Design Phase (Week 2)

This phase defines **how** the system will deliver each requirement. It is
divided into high-level architecture, detailed OOP/component design, database
schema, and UI/routing design.

### 2.1 High-Level Architecture

Define a **3-tier B/S (Browser/Server) architecture**:

```
React SPA (Vite)  →  Django REST API (DRF)  →  PostgreSQL + pgvector (Supabase)
    (Vercel)              (Render)                    (Supabase)
         ↑                                                ↑
         └── JWT auth ───────────────────────────────────┘
                             ↑
                    OpenRouter (Llama 4 Maverick)
                         RAG Chatbot Only
```

### 2.2 OOP Class & Component Design

The system is decomposed into **5 independent Django apps**, each owning its
models, serializers, views, and URL configurations. This modular design
demonstrates **Single Responsibility Principle (SRP)** and **Separation of
Concerns** — concepts directly applied from the OOP inheritance work in Week 8
(Activity 3: Single Inheritance; Activity 4: Hybrid Inheritance).

| Django App | Models (Classes) | Key Relationships |
|---|---|---|
| `accounts` | `User(AbstractUser)` with `role: STAFF\|ADMIN` | Base auth class extended from Django's built-in |
| `training` | `Module`, `Question`, `Enrollment` | Module → FK → Question; User → FK → Enrollment |
| `compliance` | `Requirement`, `ComplianceRecord` | Requirement ← FK → ComplianceRecord → FK → User |
| `incidents` | `Incident` | Incident → FK → User (reporter) |
| `chatbot` | `Document`, `Chunk` | Document → FK → Chunk (composition); Chunk.embedding = pgvector VectorField(384) |

The `chatbot.Document → Chunk` relationship is a **composition** pattern:
deleting a Document cascades to its Chunks. The `Chunk` model uses
**pgvector's VectorField** for semantic similarity search, with L2Distance
ordering for retrieval.

### 2.3 Database Schema Design

- **11 tables** across 5 apps, with explicit primary/foreign key constraints
  and indexes
- **pgvector extension** enabled on Supabase PostgreSQL for the `chunk` table's
  384-dimensional `embedding` column (produced by fastembed / BAAI/bge-small-en)
- Database connection via `psycopg`, using Supabase transaction-pooling port
  (6543) for production; SQLite fallback for local development

### 2.4 UI/UX & API Route Design

**6 UI screens:** Login → Dashboard (summary cards) → Training (list → detail →
quiz) → Compliance (status list) → Incidents (list + report form) → Chatbot
(floating widget)

**15+ REST API endpoints** across 5 route prefixes:

| Prefix | Key Endpoints |
|---|---|
| `/api/auth/` | `login/`, `refresh/`, `me/` |
| `/api/training/` | `GET /`, `GET /:id/`, `POST /enrollments/`, `POST /:id/submit/` |
| `/api/compliance/` | `GET /` (staff sees own, admin sees all) |
| `/api/incidents/` | `GET /`, `POST /`, `PATCH /:id/` |
| `/api/chatbot/` | `POST /ask/` |

All endpoints are protected by JWT authentication. Admin-only endpoints use
`IsAdminUser` permission class.

### Phase Deliverables

- *System Architecture & Design Specification (incl. Class Diagram, ERD, API Route Table)*
- *Database DDL Script (PostgreSQL + pgvector extension)*
- *UI Mockups & Wireframes for all 6 Screens*

---

## 3. Implementation / Development Phase (Weeks 3–4)

Code is written in strict accordance with the design specification. The
implementation follows a **walking-skeleton** approach: a thin end-to-end
slice is built first, then each feature is added incrementally.

### 3.1 Environment Setup & Infrastructure

- Initialise Python 3.12+ virtual environment; install dependencies: Django 5,
  DRF, SimpleJWT, psycopg, pgvector, fastembed, httpx, django-cors-headers,
  Gunicorn
- Initialise React 18 + Vite project; install React Router, Axios
- Create a Supabase PostgreSQL instance; run DDL to generate all 11 tables +
  enable pgvector extension
- Write the `seed_data` Django management command for reproducible demo data

### 3.2 Backend Development (Django + DRF)

- Implement custom `User` model extending `AbstractUser` with `STAFF | ADMIN`
  role enum
- Build all 15+ REST API endpoints: serializers → views → URL routing for each
  of the 5 apps
- Implement compliance status engine: `ComplianceRecord.compute_status()` —
  computed on read (COMPLIANT / DUE / OVERDUE), no cron job needed for MVP
- Implement quiz submission endpoint: accept `[{question_id, selected_index}]`
  → compare against `Question.correct_index` → compute score → update Enrollment
- Write seed data: 3 training modules × 3 questions, 3 compliance requirements
  with frequency days, 2 sample incidents, 5 healthcare compliance documents

### 3.3 Frontend Development (React + Vite)

- Build `AuthContext` + JWT token store in `localStorage`; Axios interceptor for
  automatic token attachment and 401 → Login redirect
- Build 6-page SPA: `LoginPage`, `Dashboard` (3 summary cards), `TrainingList` +
  `TrainingDetail` (quiz with radio buttons), `ComplianceList` (color-coded
  status badges), `IncidentList` (staff list + admin resolve button),
  `IncidentForm`
- Build `Layout` component: dark sidebar navigation (Dashboard / Training /
  Compliance / Incidents) + user info + logout
- Build `ChatWidget`: floating action button → slide-out panel → question input
  → API call → display answer + source citations

### 3.4 RAG Chatbot Pipeline

- **Ingestion:** management command `ingest_docs` reads plain-text documents →
  `_split_text()` (300-word chunks, 50-word overlap) → fastembed
  (BAAI/bge-small-en, 384-dim) → `Chunk.bulk_create()`
- **Retrieval:** embed user question → pgvector `L2Distance` similarity search →
  return top-5 Chunks with document titles
- **Generation:** build RAG prompt (system = healthcare compliance expert, use
  only context) → `httpx.post()` to OpenRouter `/chat/completions` with
  `meta-llama/llama-4-maverick:free` → return answer + source list
- **Fallback:** if OpenRouter API key missing or request fails, return raw top-3
  chunks without AI summarisation

### Phase Deliverables

- *Fully Functional Source Code (pre-deployment)*
- *Seed Data Script (3 modules, 3 requirements, 5 documents, 2 demo users)*

---

## 4. Testing & Validation Phase (Week 5)

A **code freeze** is enacted, and the project enters an intensive Quality
Assurance phase to ensure the system meets all SRS requirements.

### 4.1 Unit Testing

- Django test cases for each API endpoint: verify response status, payload
  shape, permission enforcement, edge cases (duplicate enrolment, invalid quiz
  submission)

### 4.2 Integration Testing

- Full-stack data-flow validation: React form submission → Axios POST → Django
  serializer → PostgreSQL write → GET returns updated data → React re-renders

### 4.3 Security & Permission Testing

- Verify unauthenticated requests return HTTP 401 for all protected endpoints
- Verify STAFF users cannot access admin-only endpoints (HTTP 403)
- Verify JWT token expiry (2h); verify refresh token flow

### 4.4 RAG Accuracy Evaluation

- Test 10 sample questions against the 5 seed documents
- Score each answer: does the chatbot cite the correct source document?
- Measure retrieval precision: does the top-5 chunk set contain the relevant
  passage?

### 4.5 User Acceptance Testing (UAT)

- Walk through all 10 business metrics end-to-end
- Cross-browser testing: Chrome, Firefox, Edge; responsive: desktop, tablet,
  mobile viewports

### Phase Deliverables

- *Test Plan & Test Case Specification*
- *Defect / Bug Tracking Report & Final Test Report*
- *UAT Sign-off Document*

---

## 5. Deployment & Delivery Phase (Week 6)

The stable system, having passed all tests, is deployed to production and
handed over.

### 5.1 Production Environment Configuration

- **Render:** create Web Service → connect GitHub repo → set root directory
  `healthcare_platform/backend` → configure env vars (`DATABASE_URL`,
  `SECRET_KEY`, `CORS_ORIGINS`, `OPENROUTER_API_KEY`) → auto-build
  (`pip install`, `migrate`, `seed_data`) → start Gunicorn
- **Vercel:** import GitHub repo → set root `healthcare_platform/frontend` →
  set `VITE_API_URL` to Render URL → auto-deploy on `git push`
- **Supabase:** create project → enable pgvector extension → copy connection
  string (transaction-pooling, port 6543) → paste into Render env vars

### 5.2 Launch & Verification

- Run `python manage.py ingest_docs` on Render production shell
- Smoke test: `curl POST /api/auth/login/` → receive JWT → `GET /api/training/`
  → returns 3 modules
- Open Vercel URL in browser → full user journey verification (handle Render
  cold start ~30s)

### 5.3 Documentation & Handover

- Finalise `README.md` with architecture diagram, setup guide, API docs, and
  known limitations
- Write role-specific quick-start guides (Staff / Admin)
- Document Render cold-start behaviour and OpenRouter free-tier limits

### Phase Deliverables

- *Live System: Vercel (React) + Render (Django) + Supabase (Postgres+pgvector)*
- *Complete GitHub Repository with README, Spec, and Deployment Guide*

---

## 6. Maintenance & Support Phase (Week 7)

Ongoing operational support following project delivery.

### 6.1 Exception Monitoring

- Monitor Render runtime logs for 5xx errors, slow requests
- Monitor Supabase database performance (connection count, query latency)

### 6.2 Bug Fixes & Security Updates

- Patch edge-case bugs reported post-launch
- Update Python (Django, DRF) and JavaScript (React, Vite, Axios) dependency
  packages that present security vulnerabilities

### 6.3 RAG Model Tuning

- Evaluate retrieval accuracy with real user questions
- Adjust chunk size / overlap parameters based on observed performance
- Iterate on the RAG prompt template for improved answer quality

### 6.4 Regulatory Updates

- Track changes to HIPAA / GDPR requirements
- Update the 5 knowledge-base documents when regulations change
- Re-run `ingest_docs` to refresh the vector index

### Phase Deliverables

- *Support SLA Agreement*
- *Maintenance Log (bug fixes, model updates, regulatory changes)*

---

## UML Class Diagram Reference

The OOP design principles demonstrated in this project are built on the
inheritance concepts from **Week 8**:

| Week 8 Activity | Inheritance Type | Key Concept |
|---|---|---|
| Activity 3 | **Single Inheritance** | `Flight` (base) → `DomesticFlight` (child) — shared attributes via `super().__init__()` |
| Activity 4 | **Hybrid Inheritance** | `Flight` → `DomesticFlight` + `InternationalFlight` (hierarchical) → `CodeShareFlight` (multiple) |

These concepts inform the Healthcare Platform's Django model design: `User`
extends `AbstractUser` (single inheritance); `Document` and `Chunk` form a
composition relationship; the 5-app modular structure demonstrates
component-level separation of concerns.
