from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.analytics import service
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/kpis")
def kpis(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.kpis(db)


@router.get("/modules")
def modules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.module_analysis(db)


@router.get("/classes")
def classes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.class_analysis(db)


@router.get("/distribution")
def distribution(
    module_id: int | None = None,
    class_id: int | None = None,
    period: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return service.grade_distribution(db, module_id, class_id, period)


@router.get("/periods")
def periods(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.periods(db)


@router.get("/correlations")
def correlations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.correlations(db)


@router.get("/anomalies")
def anomalies(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.anomaly_report(db)


@router.get("/segmentation")
def segmentation(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.segmentation_summary(db)


@router.get("/at-risk")
def at_risk(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.at_risk_students(db)
