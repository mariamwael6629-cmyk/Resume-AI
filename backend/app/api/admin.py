from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Resume, User
from app.schemas.schemas import AdminUserOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[AdminUserOut])
def list_users(db: Session = Depends(get_db)):
    # NOTE: stubbed without admin-role auth gate for demo purposes — in a
    # production build this should require `current_user.is_admin`.
    users = db.query(User).order_by(User.created_at.desc()).all()
    out = []
    for u in users:
        resume_count = db.query(Resume).filter(Resume.user_id == u.id).count()
        out.append(
            AdminUserOut(
                id=u.id,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                is_admin=u.is_admin,
                created_at=u.created_at,
                resume_count=resume_count,
            )
        )
    return out
