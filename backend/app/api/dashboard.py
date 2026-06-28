from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import Application, JobPosting, Resume, User
from app.schemas.schemas import DashboardOverview

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    ats_score = latest_resume.ats_score if latest_resume else 0
    resumes_analyzed = db.query(Resume).filter(Resume.user_id == current_user.id).count()

    job_matches = db.query(JobPosting).count() if latest_resume else 0
    applications_sent = (
        db.query(Application)
        .filter(Application.user_id == current_user.id, Application.status.in_(["applied", "interview"]))
        .count()
    )
    interviews_scheduled = (
        db.query(Application)
        .filter(Application.user_id == current_user.id, Application.status == "interview")
        .count()
    )

    return DashboardOverview(
        ats_score=ats_score,
        job_matches=job_matches,
        applications_sent=applications_sent,
        interviews_scheduled=interviews_scheduled,
        resumes_analyzed=resumes_analyzed,
    )
