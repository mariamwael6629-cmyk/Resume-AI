import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import BuilderDraft, User
from app.schemas.schemas import BuilderDraftOut, BuilderSaveRequest

router = APIRouter(prefix="/api/builder", tags=["builder"])


@router.post("/save", response_model=BuilderDraftOut)
def save_draft(
    payload: BuilderSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    draft = db.query(BuilderDraft).filter(BuilderDraft.user_id == current_user.id).first()
    content_str = json.dumps(payload.content)
    if draft:
        draft.content_json = content_str
    else:
        draft = BuilderDraft(user_id=current_user.id, content_json=content_str)
        db.add(draft)
    db.commit()
    db.refresh(draft)
    return BuilderDraftOut(content=json.loads(draft.content_json), updated_at=draft.updated_at)


@router.get("", response_model=BuilderDraftOut)
def get_draft(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    draft = db.query(BuilderDraft).filter(BuilderDraft.user_id == current_user.id).first()
    if not draft:
        return BuilderDraftOut(content={}, updated_at=None)
    return BuilderDraftOut(content=json.loads(draft.content_json), updated_at=draft.updated_at)
