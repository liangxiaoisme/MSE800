# Intelligent Healthcare Compliance & Safety Management Platform — Design Spec

**Status:** Approved  
**Date:** 2026-06-05  
**Stack:** React.js · Python Django · PostgreSQL + pgvector · Llama 4 Maverick (OpenRouter) · Vercel · Render · Supabase  

## 1. Goal

Working MVP demo that proves the full architecture end-to-end:
deployed, runnable, breadth over depth for a course capstone submission.

## 2. Architecture

```
Browser ──────────►  Vercel (React SPA, Vite)
                          │  HTTPS + JWT
                          ▼
                     Render (Django + DRF REST API)
                          │
              ┌───────────┼──────────────┐
              ▼           ▼              ▼
    Supabase (Postgres)  pgvector       OpenRouter
    + pgvector           (embeddings)   Llama 4 Maverick :free
```

Three free services + one free API key. All scale to zero (no cost when idle).

## 3. Repo Structure

```
healthcare_platform/
├── backend/
│   ├── config/              # settings, urls, wsgi (12-factor, env vars)
│   ├── accounts/            # custom User (role: STAFF|ADMIN), JWT auth
│   ├── training/            # modules, questions, enrollment, progress
│   ├── compliance/          # requirements, staff compliance records
│   ├── incidents/           # incident reports + status workflow
│   ├── chatbot/             # RAG: documents, chunks (+vector), retrieve, chat
│   ├── seed/                # generated sample healthcare docs + fixtures
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/             # axios client, auth interceptor
│       ├── auth/            # login page, token store, route guard
│       ├── pages/           # Dashboard, Training, Compliance, Incidents
│       ├── components/      # ChatWidget, Layout, shared UI
│       └── App.jsx
└── README.md
```

### Tech choices

**Backend:** Django 5 · DRF · djangorestframework-simplejwt · psycopg · pgvector Django field · fastembed (BAAI/bge-small-en, 384-dim) · httpx (OpenRouter) · django-cors-headers  
**Frontend:** React 18 · Vite · React Router · Axios · hand-rolled minimal CSS  
**Config:** all secrets via env vars (DATABASE_URL, OPENROUTER_API_KEY, SECRET_KEY, CORS_ORIGINS). `.env.example` committed; real `.env` git-ignored.

## 4. Data Model

```
accounts.User (extends AbstractUser)
  • role: STAFF | ADMIN     • email, name

training.Module                    training.Enrollment
  • title, description             • user → User
  • content (markdown)             • module → Module
  • pass_mark                      • status: NOT_STARTED|IN_PROGRESS|COMPLETED
                                   • score, completed_at
training.Question
  • module → Module
  • text, options (JSON), correct_index

compliance.Requirement             compliance.ComplianceRecord
  • title, description             • user → User
  • category                       • requirement → Requirement
  • frequency (days)               • status: COMPLIANT|DUE|OVERDUE
                                   • last_completed_at, due_at

incidents.Incident
  • reporter → User
  • title, description, location, severity (LOW|MED|HIGH|CRITICAL)
  • status: SUBMITTED|UNDER_REVIEW|RESOLVED
  • created_at, resolved_at

chatbot.Document                   chatbot.Chunk
  • title, source                  • document → Document
  • uploaded_by → User             • content (text)
  • created_at                     • embedding: vector(384) ← pgvector
                                   • chunk_index
```

### Roles
- **STAFF:** training, own compliance, file incidents, use chatbot.
- **ADMIN:** additionally manages modules/requirements, reviews incidents, uploads documents.

## 5. RAG Pipeline

### Ingestion (offline)
```
Admin uploads document → extract text → split into ~300-word chunks (50-word overlap)
→ embed each chunk with fastembed / bge-small-en (384-dim)
→ store in Postgres (body + vector, pgvector indexed)
```

### Query (online)
```
User asks question → embed question text
→ pgvector similarity search (top-5 chunks)
→ build prompt: system = "You are a healthcare compliance expert. Use the following context to answer..."
  + context chunks + user question
→ OpenRouter / llama-4-maverick:free → generate answer
→ return answer + source citations
```

### Fallback
If OpenRouter quota is exhausted: return the raw top-3 chunks without LLM summarization. The feature still works — just without AI polish.

## 6. MVP Scope

### In scope

| Feature | What gets built |
|---|---|
| Auth | JWT login + role-based routing; no password reset |
| Training | 3 seed modules with 3-question quizzes; staff enroll → quiz → score saved |
| Compliance | 3 seed requirements; staff dashboard shows compliant/due/overdue (computed on read) |
| Incidents | Staff submit form → saved; admin lists → changes status to RESOLVED |
| Chatbot | 5 seeder docs ingested; single-turn RAG with source citations; floating chat widget |
| Frontend | Login → Dashboard (summary cards) → sidebar-nav pages → floating Chatbot button |
| Deploy | Vercel (React) + Render (Django) + Supabase (Postgres+pgvector) + OpenRouter (LLM) |

### Out of scope (future)

- Multi-turn chatbot conversation
- Real file upload / PDF parsing (seed with plain-text docs instead)
- Staff self-registration (admin creates via Django admin)
- Analytics dashboards (summary cards only)
- Emails / push notifications
- Cron-based compliance checks (computed on read)
- Unit/integration tests

### Build order
```
Phase 1: Scaffold backend (Django project + apps + models) + seed data
Phase 2: REST APIs (auth + CRUD for training/compliance/incidents + chatbot ask endpoint)
Phase 3: RAG ingestion pipeline (fastembed + pgvector + OpenRouter chat)
Phase 4: React frontend (login + dashboard + pages + chatbot widget)
Phase 5: Deploy (Render + Vercel + Supabase + OpenRouter key)
```

## 7. Deployment Map

| Service | What | Limits to know |
|---|---|---|
| Vercel | React SPA | 100 GB/mo bandwidth |
| Render | Django REST API | Free dyno sleeps after 15 min idle; ~30s cold start |
| Supabase | PostgreSQL + pgvector | 500 MB storage |
| OpenRouter | Llama 4 Maverick | Free tier, rate-limited |

### Render cold start
Frontend fires a warm-up request on first page load → shows "Waking up server…" → retries.

### Manual steps (user does, with guide)
1. Sign up Supabase → create project → enable pgvector → copy connection string
2. Sign up Render → create Web Service → connect GitHub → set env vars
3. Sign up Vercel → import GitHub repo → set env var → auto-deploy
4. Sign up OpenRouter → copy API key → paste into Render env vars
