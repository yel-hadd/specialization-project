from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import AppClass, Module, User
from app.schemas.schemas import ClassOut, ModuleOut

router = APIRouter(tags=["catalog"])


@router.get("/classes", response_model=list[ClassOut])
def list_classes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list(db.scalars(select(AppClass).order_by(AppClass.name)).all())


@router.get("/modules", response_model=list[ModuleOut])
def list_modules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list(db.scalars(select(Module).order_by(Module.name)).all())
