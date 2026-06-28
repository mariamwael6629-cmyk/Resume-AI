from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_user_optional
from app.core.database import get_db
from app.models import Application, JobPosting, Resume, User
from app.schemas.schemas import ApplicationOut, JobOut
from app.services.job_matching import compute_match_percent

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def _job_to_out(job: JobPosting, match_percent: int | None, saved: bool, applied: bool) -> JobOut:
    return JobOut(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        job_type=job.job_type,
        employment_type=job.employment_type,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        tags=[t for t in job.tags.split(",") if t],
        description=job.description,
        posted_days_ago=job.posted_days_ago,
        match_percent=match_percent,
        saved=saved,
        applied=applied,
    )


@router.get("", response_model=list[JobOut])
def list_jobs(
    location: str | None = None,
    job_type: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    query = db.query(JobPosting)
    if location:
        query = query.filter(JobPosting.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(JobPosting.job_type.ilike(f"%{job_type}%"))
    if q:
        query = query.filter(JobPosting.title.ilike(f"%{q}%"))
    jobs = query.order_by(JobPosting.created_at.desc()).all()

    user_keywords: list[str] = []
    saved_ids: set[int] = set()
    applied_ids: set[int] = set()

    if current_user:
        latest_resume = (
            db.query(Resume)
            .filter(Resume.user_id == current_user.id)
            .order_by(Resume.created_at.desc())
            .first()
        )
        if latest_resume and latest_resume.found_keywords:
            user_keywords = [k for k in latest_resume.found_keywords.split(",") if k]

        apps = db.query(Application).filter(Application.user_id == current_user.id).all()
        saved_ids = {a.job_id for a in apps if a.status in ("saved", "applied", "interview")}
        applied_ids = {a.job_id for a in apps if a.status in ("applied", "interview")}

    out = []
    for job in jobs:
        match_percent = None
        if current_user:
            match_percent = compute_match_percent(
                job.tags.split(",") if job.tags else [], job.description, user_keywords
            )
        out.append(_job_to_out(job, match_percent, job.id in saved_ids, job.id in applied_ids))
    return out


def _get_job_or_404(db: Session, job_id: int) -> JobPosting:
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


def _get_or_create_application(db: Session, user_id: int, job_id: int) -> Application:
    app_row = (
        db.query(Application)
        .filter(Application.user_id == user_id, Application.job_id == job_id)
        .first()
    )
    if not app_row:
        app_row = Application(user_id=user_id, job_id=job_id, status="saved")
        db.add(app_row)
    return app_row


@router.post("/{job_id}/save", response_model=ApplicationOut)
def save_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_job_or_404(db, job_id)
    app_row = _get_or_create_application(db, current_user.id, job_id)
    db.commit()
    db.refresh(app_row)
    return app_row


@router.post("/{job_id}/apply", response_model=ApplicationOut)
def apply_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_job_or_404(db, job_id)
    app_row = _get_or_create_application(db, current_user.id, job_id)
    app_row.status = "applied"
    db.commit()
    db.refresh(app_row)
    return app_row
