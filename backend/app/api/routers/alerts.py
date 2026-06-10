from fastapi import APIRouter, Depends
from sqlalchemy import case, delete, select
from sqlalchemy.orm import Session

from app.analytics import service
from app.analytics.data import absences_frame, grades_frame
from app.analytics.risk import risk_table
from app.api.deps import get_current_user
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
    """Recalcule les alertes a partir des donnees actuelles. Remplace les alertes auto non resolues."""
    th = service.get_thresholds(db)
    rt = risk_table(grades_frame(db), absences_frame(db), th)

    # on purge les anciennes alertes non resolues pour repartir de l'etat courant
    db.execute(delete(Alert).where(Alert.resolved == False))  # noqa: E712

    created = 0
    for _, r in rt.iterrows():
        sid = int(r["student_id"])
        if r["average"] < th["pass_mark"]:
            db.add(Alert(
                student_id=sid, alert_type="low_average", severity=_severity(r["risk_score"]),
                message=f"Moyenne faible ({r['average']}) sous le seuil de {th['pass_mark']}.",
                threshold_value=th["pass_mark"],
            ))
            created += 1
        if r["absence_rate"] >= th["high_absence_rate"]:
            db.add(Alert(
                student_id=sid, alert_type="high_absence", severity=_severity(r["risk_score"]),
                message=f"Taux d'absence eleve ({round(r['absence_rate'] * 100, 1)}%).",
                threshold_value=th["high_absence_rate"],
            ))
            created += 1
        if r["drop"] >= th["performance_drop"]:
            db.add(Alert(
                student_id=sid, alert_type="performance_drop", severity=_severity(r["risk_score"]),
                message=f"Baisse de performance de {r['drop']} points entre periodes.",
                threshold_value=th["performance_drop"],
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
    # ordre stable: severite la plus haute d'abord, puis par etudiant,
    # comme ca regenerer les alertes ne melange pas la liste
    severity_rank = case(
        {"high": 0, "medium": 1, "low": 2}, value=Alert.severity, else_=3
    )
    stmt = select(Alert).order_by(severity_rank, Alert.student_id, Alert.alert_type)
    if resolved is not None:
        stmt = stmt.where(Alert.resolved == resolved)
    return list(db.scalars(stmt).all())
