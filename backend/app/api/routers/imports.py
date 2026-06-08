from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import ImportLog, User
from app.pipeline.runner import run_import
from app.schemas.schemas import ImportLogOut, ImportResult

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("", response_model=ImportResult)
async def create_import(
    file: UploadFile = File(...),
    type: str = Form("auto"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ImportResult:
    content = await file.read()
    result = run_import(db, file.filename or "upload", content, type)
    return ImportResult(**result)


@router.get("", response_model=list[ImportLogOut])
def list_imports(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[ImportLog]:
    return list(
        db.scalars(select(ImportLog).order_by(ImportLog.imported_at.desc())).all()
    )
