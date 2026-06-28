# Migration notes — Frontend/Backend Integration

This documents what changed when the original static, frontend-only mockup
(`ai_resume_analyzer_job_matcher.html` with hardcoded/mock data) was
extended into a full-stack system. Nothing existing was rebuilt, renamed,
or removed — a backend was added alongside the existing frontend, and the
frontend's JavaScript was extended in place to talk to it.

## What's preserved

- `ai_resume_analyzer_job_matcher.html` is still the single entry point for
  the UI — same file, same page structure (`goTo()`-based client-side
  routing between `.page` divs), same IDs/classes/function names for
  everything that existed before.
- All pre-existing screens (landing, login, register, dashboard, analyzer,
  jobs, builder, admin), styling, theming, and language toggle are
  unchanged.
- The app still works as a single HTML file you can open directly; running
  the FastAPI backend is what unlocks real persistence, auth, resume
  analysis, and job data — but if the backend isn't running, the frontend
  falls back to its original static/cached data and shows a toast, rather
  than breaking.

## What's new

- **Backend** (`backend/`): FastAPI + SQLAlchemy + SQLite, layered as
  `models/` → `schemas/` → `services/` → `api/`, assembled in
  `backend/app/main.py`. Not present before; added without touching the
  frontend's existing page markup beyond adding a handful of missing
  `id` attributes needed for the JS to read/write form fields.
- **Auth**: JWT bearer-token login/register (`/api/auth/*`), bcrypt password
  hashing. The login/register forms now call the API instead of immediately
  navigating to the dashboard with no validation.
- **Resume analysis**: `startAnalysis()` / the file upload zone now POST to
  `/api/resumes/upload` and render the real response (ATS score, found/
  missing keywords, suggestions) instead of revealing canned data after a
  fake `setTimeout`.
- **Jobs**: the Job Matcher page fetches real seeded job postings from
  `/api/jobs`, with save/apply wired to `/api/jobs/{id}/save` and
  `/api/jobs/{id}/apply`.
- **Dashboard**: overview metrics load from `/api/dashboard/overview`.
- **Resume Builder**: save/load wired to `/api/builder`.
- **Admin panel**: the Users tab now loads real registered users from
  `/api/admin/users` instead of 4 hardcoded rows.
- **Graceful degradation**: every fetch is wrapped so that if the backend
  is unreachable, the UI shows a toast ("Could not reach server — showing
  cached …") and falls back to static placeholder data instead of
  crashing.

## Data migration

There is no data to migrate from the old prototype — it held no real
persisted data (everything lived in hardcoded HTML/JS, lost on refresh).
First boot of the backend starts from an empty SQLite database, auto-seeded
only with ~15 mock job postings (see `backend/app/db/seed.py`). Creating an
account via the Register page is how you get a real user to test with.

## Backend route layout

All API routes are namespaced under `/api/*` and documented interactively
at `/docs` (Swagger UI) and `/redoc` once the backend is running — see the
README's [API Reference](./README.md#-api-reference) section for the
resource summary.

## Known stubs / limitations

- ATS scoring (`backend/app/services/resume_analysis.py`) and job matching
  (`backend/app/services/job_matching.py`) are deterministic heuristic
  stubs (keyword/pattern matching), not real ML/NLP — flagged in code
  comments.
- Resume uploads are read as text; PDF/DOCX binary content isn't parsed,
  so non-plain-text uploads will score poorly. Fine for this mockup's
  scope, but a real product would need an actual PDF/DOCX text extractor.
- `/api/admin/users` has no admin-role gate yet — anyone with a valid token
  (or no token, depending on deployment) can read the list.
