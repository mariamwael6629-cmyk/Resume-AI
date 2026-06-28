# 🚀 ResumeAI — AI-Powered Career Platform

ResumeAI is a full-stack career platform that helps job seekers optimize
their resumes for Automated Screening Systems (ATS), discover skill gaps,
track application progress, and match instantly with relevant job openings.

---

## ✨ Key Features

### 1. AI Resume Analysis & ATS Scoring
* **Instant Scoring:** Upload a resume to receive an ATS compatibility score, found vs. missing keywords, and actionable suggestions.
* **Persisted history:** Each analysis is saved to your account via the backend API.

### 2. Smart Job Matcher
* **Real job postings:** Browse seeded job listings with match-percentage scoring against your profile.
* **Filters:** Filter by location, job type, or keyword; save or apply to jobs with one click.

### 3. Resume Builder
* **Save & resume drafting:** Build a structured resume (summary, experience, skills) that persists across sessions via the backend.

### 4. Dashboard & Admin
* **Dashboard:** Overview metrics (analyses run, scores, saved/applied jobs) loaded from the API.
* **Admin Panel:** View all registered users and their resume counts.

### 5. Bilingual UI & Theming
* Language toggle (EN/AR) and light/dark theming, unchanged from the original mockup.

---

## 🛠️ Tech Stack & Architecture

* **Frontend:** Single-file vanilla JS/HTML/CSS app (`resume_ai.html`) — no build step, no framework. Client-side routing via `goTo()` toggling `.page` sections.
* **Backend:** Python, FastAPI + SQLAlchemy, SQLite (file-based DB, no separate DB server to install). Layered as `models/` → `schemas/` → `services/` → `api/`, assembled in `backend/app/main.py`.
* **Auth:** JWT bearer tokens (PyJWT) + bcrypt password hashing (passlib).
* **API docs:** Auto-generated interactive Swagger UI at `/docs` and ReDoc at `/redoc` once the backend is running — every endpoint is documented there, including request/response schemas.
* **Resume/job matching:** Deterministic heuristic stubs (keyword/pattern matching), not real ML/NLP — see [Known stubs](./MIGRATION.md#known-stubs--limitations) in `MIGRATION.md`.

---

## 💰 Pricing Tiers

| Tier | Price | Highlights |
| :--- | :--- | :--- |
| **Free** | $0 / mo | 3 analyses/month, Basic ATS score, 10 job matches. |
| **Pro** | $19 / mo | Unlimited analyses/matches, Advanced ATS optimization, AI Recommendations, Builder access (+20 templates), Priority support. |
| **Enterprise** | $89 / mo | Everything in Pro, Team dashboard, API access, Custom branding, Dedicated success manager. |

---

## 📋 Frequently Asked Questions (FAQ)

* **What file formats does ResumeAI support?** Resumes are currently read as plain text; PDF/DOCX binary parsing is not yet implemented (see `MIGRATION.md`).
* **Is my resume data kept private?** Data is stored locally in the backend's SQLite database; no third-party services are used.
* **Does ResumeAI support Arabic resumes?** The UI supports an English/Arabic language toggle.

---

## 🚀 Installation & Local Setup

### Requirements

- Python 3.9+
- A modern browser (Chrome/Edge/Firefox/Safari)

### 1. Clone the repository

```bash
git clone https://github.com/mariamwael6629-cmyk/resume-ai.git
cd resume-ai
```

### 2. Set up and run the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # adjust values if needed
uvicorn app.main:app --reload --port 8000
```

The first run creates the SQLite database automatically and seeds it with
~15 mock job postings (see [Test/seed data](#-testseed-data) below).

### 3. Open the app

- API (FastAPI backend): **http://127.0.0.1:8000/**
- Interactive API docs (Swagger UI): **http://127.0.0.1:8000/docs**
- ReDoc: **http://127.0.0.1:8000/redoc**
- Frontend: open `resume_ai.html` directly in a browser,
  or serve it (e.g. `python3 -m http.server 5500`) and visit
  `http://127.0.0.1:5500/resume_ai.html`.

The frontend talks to the API at `http://localhost:8000` by default (see
`API_BASE` near the top of the `<script>` block). If the backend isn't
running, the UI falls back to static/cached data and shows a toast instead
of breaking — see [`MIGRATION.md`](./MIGRATION.md) for details.

Register a new account via the **Register** page to get a real user to test
with — there's no pre-seeded login.

---

## 📖 API Reference

All endpoints are namespaced under `/api/*` and fully documented (with
parameters and example responses) in the interactive Swagger UI at `/docs`
once the backend is running. Summary of resource groups:

| Resource | Base path | Notes |
|---|---|---|
| Auth | `/api/auth/register`, `/api/auth/login`, `/api/auth/me` | JWT bearer-token issuance/validation |
| Resumes | `/api/resumes/upload`, `/api/resumes` | Multipart upload, returns ATS score/keywords/suggestions |
| Jobs | `/api/jobs`, `/api/jobs/{id}/save`, `/api/jobs/{id}/apply` | Filters: `location`, `job_type`, `q` |
| Builder | `/api/builder` (GET/POST) | Save/load a resume draft |
| Dashboard | `/api/dashboard/overview` | Aggregate metrics for the dashboard page |
| Admin | `/api/admin/users` | List registered users (no admin-role gate yet) |

---

## 🧪 Test/seed data

- **Job postings** are seeded automatically on first boot
  (`backend/app/db/seed.py`, runs from `app/main.py` only if the table is
  empty) — this is what powers the Job Matcher page out of the box.
- **Users** are *not* pre-seeded — register a real account via the app's
  Register page.

---

## 🔄 Migration notes

See [`MIGRATION.md`](./MIGRATION.md) for what changed when the original
static `resume_ai.html` mockup was extended with a real
backend, and what's preserved vs. new.
