from fastapi import APIRouter, Depends
from sqlalchemy import case, delete, select
from sqlalchemy.orm import Session

from app.analytics import service
from app.analytics.data import absences_frame, grades_frame
from app.analytics.risk import risk_table
from app.api.deps import get_current_user
from app.core import messages
from app.core.database import get_db
from app.models import Alert, User
from app.schemas.schemas import AlertOut

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _severity(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


@router.post("/generate")
def generate_alerts(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Recompute alerts from current data, replacing unresolved auto alerts."""
    th = service.get_thresholds(db)
    rt = risk_table(grades_frame(db), absences_frame(db), th)

    # purge old unresolved alerts so we restart from the current state
    db.execute(delete(Alert).where(Alert.resolved == False))  # noqa: E712

    created = 0
    for _, r in rt.iterrows():
        sid = int(r["student_id"])
        sev = _severity(r["risk_score"])
        # `message` stores a French rendering for the report and any non-UI consumer;
        # the frontend re-renders from alert_type + threshold_value + metric_value.
        if r["average"] < th["pass_mark"]:
            db.add(Alert(
                student_id=sid, alert_type="low_average", severity=sev,
                message=messages.alert_text(
                    "low_average", "fr", value=r["average"], threshold=th["pass_mark"]
                ),
                threshold_value=th["pass_mark"], metric_value=float(r["average"]),
            ))
            created += 1
        if r["absence_rate"] >= th["high_absence_rate"]:
            db.add(Alert(
                student_id=sid, alert_type="high_absence", severity=sev,
                message=messages.alert_text(
                    "high_absence", "fr", value=round(r["absence_rate"] * 100, 1)
                ),
                threshold_value=th["high_absence_rate"], metric_value=float(r["absence_rate"]),
            ))
            created += 1
        if r["drop"] >= th["performance_drop"]:
            db.add(Alert(
                student_id=sid, alert_type="performance_drop", severity=sev,
                message=messages.alert_text("performance_drop", "fr", value=r["drop"]),
                threshold_value=th["performance_drop"], metric_value=float(r["drop"]),
            ))
            created += 1

    db.commit()
    return {"created": created}


@router.get("", response_model=list[AlertOut])
def list_alerts(
    resolved: bool | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    # stable order: highest severity first, then by student, so regenerating
    # alerts does not reshuffle the list
    severity_rank = case(
        {"high": 0, "medium": 1, "low": 2}, value=Alert.severity, else_=3
    )
    stmt = select(Alert).order_by(severity_rank, Alert.student_id, Alert.alert_type)
    if resolved is not None:
        stmt = stmt.where(Alert.resolved == resolved)
    return list(db.scalars(stmt).all())
