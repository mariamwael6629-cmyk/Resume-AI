# ResumeAI Backend

FastAPI backend for the ResumeAI frontend mockup. SQLite-based, no external
services required.

## Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # already provided with a dev secret; edit as needed
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

(Or from the repo root: `uvicorn app.main:app --reload --port 8000 --app-dir backend`)

The database (`resumeai.db`) and ~15 seed job postings are created automatically on startup.

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- ATS scoring (`app/services/resume_analysis.py`) and job matching
  (`app/services/job_matching.py`) are deterministic heuristic stubs, not
  real ML — see in-code comments.
- Auth uses JWT bearer tokens (python-jose) with bcrypt password hashing.
- CORS is wide-open (`CORS_ORIGINS=*` in `.env`) for local frontend development.
