from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import Resume, User
from app.schemas.schemas import ResumeAnalysisOut
from app.services.resume_analysis import analyze_resume_text

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


def _resume_to_out(resume: Resume) -> ResumeAnalysisOut:
    return ResumeAnalysisOut(
        id=resume.id,
        filename=resume.filename,
        ats_score=resume.ats_score,
        formatting_score=resume.formatting_score,
        keywords_score=resume.keywords_score,
        experience_score=resume.experience_score,
        education_score=resume.education_score,
        found_keywords=[k for k in resume.found_keywords.split(",") if k],
        missing_keywords=[k for k in resume.missing_keywords.split(",") if k],
        suggestions=[s for s in resume.suggestions.split("\n") if s],
        created_at=resume.created_at,
    )


@router.post("/upload", response_model=ResumeAnalysisOut, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    raw_bytes = await file.read()
    # Best-effort text decode; non-text formats (real PDF/DOCX) would need a
    # real parser in production. For this stub we just decode what we can.
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    result = analyze_resume_text(text, filename=file.filename or "resume")

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename or "resume",
        raw_text_excerpt=text[:2000],
        ats_score=result["ats_score"],
        formatting_score=result["formatting_score"],
        keywords_score=result["keywords_score"],
        experience_score=result["experience_score"],
        education_score=result["education_score"],
        found_keywords=",".join(result["found_keywords"]),
        missing_keywords=",".join(result["missing_keywords"]),
        suggestions="\n".join(result["suggestions"]),
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return _resume_to_out(resume)


@router.get("", response_model=list[ResumeAnalysisOut])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    return [_resume_to_out(r) for r in resumes]
