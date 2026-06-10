from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics import service
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import Student, User
from app.schemas.schemas import StudentDetail, StudentOut

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentOut])
def list_students(
    class_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = select(Student).order_by(Student.last_name, Student.first_name)
    if class_id is not None:
        stmt = stmt.where(Student.class_id == class_id)
    return list(db.scalars(stmt).all())


@router.get("/{student_id}", response_model=StudentDetail)
def student_detail(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    detail = service.student_detail(db, student_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Etudiant introuvable")
    return detail
