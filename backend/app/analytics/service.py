"""Couche d'orchestration : transforme les donnees de la base en payloads renvoyes par l'API."""

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics import anomalies, correlation, descriptive, risk
from app.analytics.data import absences_frame, grades_frame, students_frame
from app.core.config import settings
from app.models import Setting

DEFAULT_THRESHOLDS = {
    "pass_mark": settings.pass_mark,
    "high_absence_rate": settings.high_absence_rate,
    "performance_drop": settings.performance_drop,
    "expected_hours": settings.expected_hours,
}


def get_thresholds(db: Session) -> dict:
    """Seuils issus de la table settings, avec repli sur les valeurs par defaut."""
    values = {s.key: s.value for s in db.scalars(select(Setting)).all()}
    return {**DEFAULT_THRESHOLDS, **values}


def kpis(db: Session) -> dict:
    grades = grades_frame(db)
    absences = absences_frame(db)
    students = students_frame(db)
    th = get_thresholds(db)

    if grades.empty:
        return {
            "n_students": int(len(students)),
            "n_grades": 0,
            "overall_average": None,
            "success_rate": None,
            "absence_rate": None,
            "n_at_risk": 0,
            "progression": None,
        }

    overall_avg = round(float(grades["value"].mean()), 2)
    per_student_avg = grades.groupby("student_id")["value"].mean()
    success_rate = round(float((per_student_avg >= th["pass_mark"]).mean()), 3)

    total_abs = float(absences["hours"].sum()) if not absences.empty else 0.0
    n_students = max(1, int(students["id"].nunique()) if not students.empty else 1)
    absence_rate = round(total_abs / (n_students * th["expected_hours"]), 3)

    rt = risk.risk_table(grades, absences, th)
    n_at_risk = int((rt["segment"].isin(["a_risque", "fragile"])).sum()) if not rt.empty else 0

    # progression globale : variation de la moyenne de la promo entre la premiere
    # et la derniere periode (positif = amelioration). None s'il n'y a qu'une periode.
    progression = None
    if grades["period"].notna().any():
        per_period = (
            grades.dropna(subset=["period"]).groupby("period")["value"].mean().sort_index()
        )
        if len(per_period) >= 2:
            progression = round(float(per_period.iloc[-1] - per_period.iloc[0]), 2)

    return {
        "n_students": int(len(students)),
        "n_grades": int(len(grades)),
        "overall_average": overall_avg,
        "success_rate": success_rate,
        "absence_rate": absence_rate,
        "n_at_risk": n_at_risk,
        "progression": progression,
    }


def module_analysis(db: Session) -> list[dict]:
    th = get_thresholds(db)
    return descriptive.by_module(grades_frame(db), th["pass_mark"])


def class_analysis(db: Session) -> list[dict]:
    th = get_thresholds(db)
    return descriptive.by_class(grades_frame(db), th["pass_mark"])


def grade_distribution(
    db: Session,
    module_id: int | None = None,
    class_id: int | None = None,
    period: str | None = None,
) -> dict:
    """Distribution des notes, filtrable par module, classe et/ou periode."""
    grades = grades_frame(db)
    if not grades.empty:
        if module_id is not None:
            grades = grades[grades["module_id"] == module_id]
        if class_id is not None:
            grades = grades[grades["class_id"] == class_id]
        if period is not None:
            grades = grades[grades["period"] == period]
    return descriptive.distribution(grades)


def periods(db: Session) -> list[str]:
    """Periodes d'evaluation distinctes presentes dans les donnees, triees."""
    grades = grades_frame(db)
    if grades.empty:
        return []
    return sorted(p for p in grades["period"].dropna().unique().tolist())


def correlations(db: Session) -> dict:
    table = correlation.student_feature_table(grades_frame(db), absences_frame(db))
    return correlation.correlation_matrix(table)


def anomaly_report(db: Session) -> dict:
    grades = grades_frame(db)
    absences = absences_frame(db)
    return {
        "grade_outliers": anomalies.grade_outliers(grades),
        "absence_outliers": anomalies.absence_outliers(absences),
    }


def segmentation_summary(db: Session) -> dict:
    """Effectifs par segment (utilise sur le tableau de bord)."""
    th = get_thresholds(db)
    rt = risk.risk_table(grades_frame(db), absences_frame(db), th)
    if rt.empty:
        return {"counts": {}, "students": []}
    counts = rt["segment"].value_counts().to_dict()
    return {"counts": {k: int(v) for k, v in counts.items()}}


def at_risk_students(db: Session) -> list[dict]:
    th = get_thresholds(db)
    grades = grades_frame(db)
    rt = risk.risk_table(grades, absences_frame(db), th)
    if rt.empty:
        return []
    students = students_frame(db).set_index("id")
    rt = rt[rt["segment"].isin(["a_risque", "fragile"])].sort_values(
        "risk_score", ascending=False
    )
    out = []
    for _, r in rt.iterrows():
        sid = int(r["student_id"])
        s = students.loc[sid] if sid in students.index else None
        out.append(
            {
                "student_id": sid,
                "student_code": s["student_code"] if s is not None else str(sid),
                "name": f"{s['first_name']} {s['last_name']}" if s is not None else "",
                "class_name": s["class_name"] if s is not None else None,
                "average": r["average"],
                "absence_rate": r["absence_rate"],
                "risk_score": r["risk_score"],
                "segment": r["segment"],
                "recommendations": risk.recommendations(r.to_dict(), th),
            }
        )
    return out


def student_detail(db: Session, student_id: int) -> dict | None:
    th = get_thresholds(db)
    grades = grades_frame(db)
    absences = absences_frame(db)
    students = students_frame(db)

    srow = students[students["id"] == student_id]
    if srow.empty:
        return None
    srow = srow.iloc[0]

    g = grades[grades["student_id"] == student_id]
    a = absences[absences["student_id"] == student_id]
    average = round(float(g["value"].mean()), 2) if not g.empty else None
    absence_hours = round(float(a["hours"].sum()), 1) if not a.empty else 0.0
    absence_rate = round(absence_hours / th["expected_hours"], 3) if th["expected_hours"] else 0.0

    # rang dans la classe selon la moyenne
    rank = class_size = None
    if not g.empty and pd.notna(srow["class_id"]):
        peers = grades[grades["class_id"] == srow["class_id"]]
        means = peers.groupby("student_id")["value"].mean().sort_values(ascending=False)
        class_size = int(len(means))
        rank = int(list(means.index).index(student_id) + 1) if student_id in means.index else None

    rt = risk.risk_table(g, a, th)
    segment = rt.iloc[0]["segment"] if not rt.empty else "moyen"
    risk_row = rt.iloc[0].to_dict() if not rt.empty else {"average": average or 0}

    return {
        "student": {
            "id": int(srow["id"]),
            "student_code": srow["student_code"],
            "first_name": srow["first_name"],
            "last_name": srow["last_name"],
            "email": None,
            "class_id": int(srow["class_id"]) if pd.notna(srow["class_id"]) else None,
        },
        "class_name": srow["class_name"] if pd.notna(srow["class_name"]) else None,
        "average": average,
        "absence_hours": absence_hours,
        "absence_rate": absence_rate,
        "rank": rank,
        "class_size": class_size,
        "risk_segment": segment,
        "grades": [
            {
                "id": int(r["id"]),
                "module_id": int(r["module_id"]),
                "value": float(r["value"]),
                "assessment_type": r["assessment_type"],
                "period": r["period"],
                "date": None,
            }
            for _, r in g.iterrows()
        ],
        "absences": [
            {
                "id": int(r["id"]),
                "module_id": None,
                "date": r["date"],
                "hours": float(r["hours"]),
                "type": r["type"],
                "justified": bool(r["justified"]),
            }
            for _, r in a.iterrows()
        ],
        "progression": risk.progression_for_student(grades, student_id),
        "recommendations": risk.recommendations(risk_row, th),
    }
