# Week 9 — Activity 2: Agile Project Management

**Project:** Intelligent Healthcare Compliance & Safety Management System  
**Group:** W  
**Team:** Abu Sufian · Xiao Liang  
**Methodology:** Agile Scrum  
**Duration:** 7 Weeks (3 Sprints × 2 Weeks + 1 Release Week)

---

## Overview

This document records the Agile project management plan for the Healthcare
Compliance Platform. It defines 3 sprints, each with clear objectives, tasks,
deliverables, sprint reviews, and retrospectives.

Agile was chosen because the project integrates multiple unfamiliar technologies
(Django, React, pgvector, RAG, OpenRouter, free cloud deployment) where
requirements may evolve as we learn. Delivering working software every 2 weeks
reduces integration risk. The 7th week is reserved for final deployment, user
training, stakeholder demo, and project retrospective.

---

## Timeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Sprint 1         Sprint 2         Sprint 3         ★ Release          │
│  Week 1–2         Week 3–4         Week 5–6         Week 7             │
│  Foundation       Integration      Hardening        Deploy & Close     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Scrum Setup

| Element | Detail |
|---|---|
| **Sprint length** | 2 weeks |
| **Total sprints** | 3 |
| **Scrum events** | Sprint Planning (Day 1), Daily Standup (async via chat), Sprint Review + Retrospective (last day) |
| **Product Backlog** | Maintained in GitHub Issues (10 user stories) |
| **Definition of Done** | Code committed, manually tested against acceptance criteria, no regressions |

---

## Sprint 1: Foundation & Backend APIs

**Duration:** Weeks 1–2  
**Sprint Goal:** Scaffold the full-stack skeleton — Django project with all models,
JWT authentication, and core REST APIs functional and testable.

### Objectives

- Set up the Django project with a modular 5-app architecture
- Define all 11 database models (accounts, training, compliance, incidents, chatbot)
- Implement JWT login with role-based access (STAFF vs ADMIN)
- Build CRUD APIs for training, compliance, and incidents
- Seed the database with realistic demo data

### Tasks

| ID | Task | Assigned | Status |
|---|---|---|---|
| 1.1 | Scaffold Django project + settings (12-factor, env vars, CORS) | Xiao Liang | Done |
| 1.2 | Create `accounts` app with custom User model (role: STAFF/ADMIN) | Xiao Liang | Done |
| 1.3 | Create `training` app: Module, Question, Enrollment models | Abu Sufian | Done |
| 1.4 | Create `compliance` app: Requirement, ComplianceRecord models | Abu Sufian | Done |
| 1.5 | Create `incidents` app: Incident model with severity/status enums | Xiao Liang | Done |
| 1.6 | Create `chatbot` app: Document, Chunk models with pgvector VectorField | Xiao Liang | Done |
| 1.7 | Implement JWT auth endpoints (login, refresh, /me) | Xiao Liang | Done |
| 1.8 | Build training API: module list/detail, enrollment, quiz submission | Abu Sufian | Done |
| 1.9 | Build compliance API: requirement list + computed status on read | Abu Sufian | Done |
| 1.10 | Build incidents API: staff create + list, admin update status | Xiao Liang | Done |
| 1.11 | Create seed management command (3 modules, 3 requirements, 2 incidents) | Abu Sufian | Done |
| 1.12 | Create 5 seed healthcare compliance documents (.txt) | Xiao Liang | Done |

### Deliverable

A working Django API server with all endpoints functional. Verified via:
- `POST /api/auth/login/` → returns JWT access + refresh tokens
- `GET /api/training/` → returns 3 modules
- `POST /api/training/1/submit/` → grades quiz, returns score
- `GET /api/compliance/` → returns compliance records with computed status
- `POST /api/incidents/` → creates incident as authenticated staff
- `PATCH /api/incidents/1/` → admin marks incident RESOLVED

### Sprint Review (end of Week 2)

**Outcome:** All 7 API endpoints functional. Database schema validated. Seed data
produces a realistic demo scenario (2 staff, 3 modules, 3 requirements, 2 incidents).

### Sprint 1 Retrospective

**What went well:**
- Django + DRF scaffold was fast; the 5-app modular structure kept code organised
- pgvector integration worked on first attempt
- Seed data made manual testing efficient — no need to create test data per session

**To improve:**
- Add request validation earlier (some serializers were written after views)
- Start frontend planning during Sprint 1 rather than waiting for Sprint 2
- Write API documentation alongside code (DRF's built-in schema browser is free)

**Action items for Sprint 2:**
- Set up Vite + React project on Day 1 of Sprint 2
- Enable DRF schema docs for reference during frontend development
- Pair-program the chatbot `/ask/` endpoint to align on request/response shape

---

## Sprint 2: Frontend + RAG Chatbot

**Duration:** Weeks 3–4  
**Sprint Goal:** Build the React SPA (login, dashboard, training, compliance,
incidents) consuming the Sprint 1 APIs, and implement the RAG chatbot pipeline
with document ingestion, pgvector retrieval, and OpenRouter answer generation.

### Objectives

- Scaffold React + Vite project with routing and API client
- Build all 6 pages: Login, Dashboard, Training (list + detail/quiz), Compliance, Incidents (list + form)
- Implement RAG ingestion: chunking → fastembed embedding → pgvector storage
- Implement RAG query: embed question → pgvector search → OpenRouter → answer
- Build floating ChatWidget component

### Tasks

| ID | Task | Assigned | Status |
|---|---|---|---|
| 2.1 | Scaffold React + Vite + React Router + Axios project | Xiao Liang | Done |
| 2.2 | Create API client with JWT interceptor (auto-attach token, 401→login) | Xiao Liang | Done |
| 2.3 | Build AuthContext (token store, user state, login/logout, role) | Xiao Liang | Done |
| 2.4 | Build LoginPage (username/password form, error handling) | Xiao Liang | Done |
| 2.5 | Build Layout component (sidebar nav, header, Outlet) | Abu Sufian | Done |
| 2.6 | Build Dashboard page (summary cards from 3 API calls) | Abu Sufian | Done |
| 2.7 | Build TrainingList + TrainingDetail + quiz submission flow | Xiao Liang | Done |
| 2.8 | Build ComplianceList (status badges: COMPLIANT/DUE/OVERDUE) | Abu Sufian | Done |
| 2.9 | Build IncidentList + IncidentForm (staff report, admin resolve) | Abu Sufian | Done |
| 2.10 | Implement document chunking logic (300 words, 50-word overlap) | Xiao Liang | Done |
| 2.11 | Implement fastembed integration (BAAI/bge-small-en, 384-dim) | Xiao Liang | Done |
| 2.12 | Implement pgvector retrieval (L2Distance similarity, top-5 chunks) | Xiao Liang | Done |
| 2.13 | Implement OpenRouter chat (Llama 4 Maverick, RAG prompt template) | Xiao Liang | Done |
| 2.14 | Implement fallback (return raw chunks if API key missing or error) | Xiao Liang | Done |
| 2.15 | Build ChatWidget (floating button, slide-out panel, send/response) | Abu Sufian | Done |
| 2.16 | Create `ingest_docs` management command for seed documents | Xiao Liang | Done |
| 2.17 | Full integration test: login → train → compliance → incident → chatbot | Both | Done |

### Deliverable

Full-stack app running locally: React SPA on :5173 ↔ Django API on :8000.
RAG chatbot answers healthcare safety questions with source citations.

### Sprint Review (end of Week 4)

**Outcome:** Complete demo walkthrough successful:
1. Login as `nurse_zhang` → Dashboard shows "Training: 3 modules"
2. Open "Hand Hygiene" module → take 3-question quiz → score 67% displayed
3. Compliance page shows "Infection Control: OVERDUE" badge
4. Report new incident → appears in list; admin logs in → marks RESOLVED
5. Chatbot: "How do I handle a needlestick injury?" → returns sourced answer

### Sprint 2 Retrospective

**What went well:**
- React + Vite integration was smooth; Axios interceptor pattern worked cleanly
- ChatWidget floating UI looks professional and matches modern chat UX
- RAG pipeline (chunk → embed → search → prompt → generate) works end-to-end
- fastembed's bge-small-en model fits within Render's 512MB free RAM perfectly
- Fallback mechanism proved itself: returns raw chunks gracefully when API key absent

**To improve:**
- OpenRouter free tier response time (~3 seconds) needs a loading indicator
- CORS configuration between Vite dev server and Django needed better documentation
- Compliance page could benefit from filtering by category or status
- Chatbot should handle empty retrieval results with a clearer user-facing message

**Action items for Sprint 3:**
- Add loading skeleton / spinner for chatbot responses
- Show "Waking up server…" message for Render cold starts in frontend
- Write deployment guide before starting deployment tasks
- Polish responsive layout for mobile-width screens

---

## Sprint 3: Deployment & Polish

**Duration:** Weeks 5–6  
**Sprint Goal:** Deploy the platform live on free cloud services, complete
end-to-end testing, polish the UI, and finalise all project documentation.

### Objectives

- Deploy Django API to Render (Gunicorn, environment variables, auto-migration)
- Deploy React SPA to Vercel (VITE_API_URL, SPA rewrite rules)
- Provision Supabase PostgreSQL database with pgvector extension
- Configure OpenRouter API key on Render
- Run document ingestion on the live server
- Perform full end-to-end user flow testing on the live deployment
- Polish UI: loading states, error boundaries, responsive layout

### Tasks

| ID | Task | Assigned | Status |
|---|---|---|---|
| 3.1 | Create Render deployment config (render.yaml, gunicorn, build command) | Xiao Liang | Done |
| 3.2 | Create Vercel deployment config (vercel.json SPA rewrites) | Xiao Liang | Done |
| 3.3 | Sign up Supabase → create project → enable pgvector → get DATABASE_URL | Abu Sufian | Done |
| 3.4 | Deploy backend to Render (connect GitHub, set env vars, trigger build) | Xiao Liang | Done |
| 3.5 | Deploy frontend to Vercel (connect GitHub, set VITE_API_URL, trigger deploy) | Xiao Liang | Done |
| 3.6 | Run `ingest_docs` on Render production instance | Xiao Liang | Done |
| 3.7 | Verify all API endpoints on live Render URL with curl | Abu Sufian | Done |
| 3.8 | Full user-flow test on live Vercel deployment | Both | Done |
| 3.9 | Fix CORS, cold-start UX, and any deployment-specific issues | Xiao Liang | Done |
| 3.10 | Polish responsive layout (mobile + tablet breakpoints) | Abu Sufian | Done |
| 3.11 | Add loading states and error boundaries to all pages | Abu Sufian | Done |
| 3.12 | Create `.env.example` with all required variables documented | Xiao Liang | Done |
| 3.13 | Final commit: update README, verify all docs, push to GitHub | Both | Done |

### Deliverable

Live deployed system accessible via public URLs:
- **Frontend:** `https://healthcare-compliance.vercel.app`
- **Backend API:** `https://healthcare-compliance-api.onrender.com`
- **Database:** Supabase PostgreSQL (managed, 500MB free tier)
- **Chatbot:** RAG pipeline with Llama 4 Maverick via OpenRouter

### Sprint Review (end of Week 6)

**Outcome:** Live demo accessible from any browser:
1. Open Vercel URL → login page loads (Render wakes from cold start ~30s)
2. Full user journey works: login → dashboard → training → compliance → incident → chatbot
3. RAG chatbot returns sourced, relevant answers on production
4. All 3 free cloud services operational at zero cost
5. GitHub repository is clean, documented, and ready for submission

### Sprint 3 Retrospective

**What went well:**
- All 3 free services deploy from a single `git push` — Render auto-builds, Vercel auto-deploys
- Supabase pgvector "just works" — no configuration beyond enabling the extension
- The walking-skeleton approach paid off: integration risks were found and fixed in Sprint 1, not Sprint 3
- Final project is live, documented, and demo-ready

**To improve:**
- Render free-tier cold start (~30 seconds on first request) is the biggest UX friction
- OpenRouter free quota limits concurrent requests — not an issue for a demo, but would be for real use
- No CI/CD automated tests — adding GitHub Actions for linting and API smoke tests would improve quality

**Action items (beyond MVP):**
- Add Render cron job to keep dyno warm (if supported on free tier)
- Consider upgrading OpenRouter to a paid tier for faster, more reliable inference
- Document known free-tier limitations prominently in README
- Add GitHub Actions workflow for automated lint + build check on PR

---

## Release Week 7: Deploy, Train &amp; Retrospect

**Focus Areas:**

- **Production cloud deployment** — Render (Django + Gunicorn), Vercel (React SPA), Supabase (PostgreSQL + pgvector)
- **User training &amp; documentation** — README, deployment guide, .env.example for all services
- **Stakeholder demo &amp; sign-off** — Live walkthrough of the full user journey
- **Project retrospective &amp; closure** — Lessons learned, what worked, what to improve
- **Final GitHub repository polish** — Clean commits, consistent naming, all docs linked

**Final Deliverable:** Live, compliant &amp; supported healthcare safety system — deployed, documented, and demo-ready.

---

## Project Outcomes

| Outcome | Evidence |
|---|---|
| Working full-stack application | Live Vercel + Render deployment |
| AI-powered RAG chatbot | Answers healthcare safety questions with source citations |
| Modular Django backend | 5 apps, clean separation of concerns |
| Modern React frontend | 6 pages, sidebar navigation, floating chatbot |
| Zero-cost deployment | 3 free cloud services + 1 free API (OpenRouter) |
| Comprehensive documentation | Spec, plan, README, Sprint records, Retrospectives |

---

## Scrum Artifacts

| Artifact | Location |
|---|---|
| Product Backlog | GitHub Issues (10 user stories) |
| Sprint Backlogs | This README (tasks per sprint) |
| Sprint Review notes | This README (outcomes per sprint) |
| Sprint Retrospective notes | This README (retrospectives per sprint) |
| Burndown / Velocity | Not tracked (2-person team, async) |

---

## Agile vs Waterfall Comparison

| Aspect | Waterfall (Activity 1) | Agile Scrum (This Activity) |
|---|---|---|
| Phases | 6 sequential phases (Waterfall) | 3 Sprints + 1 Release Week (Agile) |
| Feedback | After all 6 phases complete | After every 2-week sprint |
| Documentation | Heavy upfront (SRS, Design Doc) | Light, just-in-time (this README) |
| Risk | Integration risks accumulate until Testing | Integration risks caught in Sprint 1 |
| Best for | Regulated environments, fixed requirements | Evolving requirements, learning new tech |
| Timeline | 7 Weeks, 6 phases | 7 Weeks, 3 sprints + release |
| Our project | Used as the SDLC framework (planning) | Used as the execution method (building code) |
