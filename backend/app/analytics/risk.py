"""Rule-based risk scoring and student segmentation.

The score (0-100) is a weighted blend of three signals:
  - low average relative to the pass mark (weight 50)
  - high absence rate relative to expected hours (weight 30)
  - performance drop between the first and last period (weight 20)
The 50/30/20 split makes the average the dominant driver while still letting
absences and a declining trend push borderline students up. The score then maps
to a segment: excellent, stable, moyen, fragile, a_risque.
"""

import pandas as pd

from app.analytics.util import ordered_periods


def _period_progression(g: pd.DataFrame) -> list[dict]:
    """Compute one student's average per period, in chronological order."""
    if g.empty or "period" not in g.columns or g["period"].isna().all():
        return []
    means = g.dropna(subset=["period"]).groupby("period")["value"].mean().round(2)
    return [
        {"period": p, "average": float(means[p])}
        for p in ordered_periods(g)
        if p in means.index
    ]


def _drop(progression: list[dict]) -> float:
    """Return points lost between the first and last period (0 if improving)."""
    if len(progression) < 2:
        return 0.0
    return max(0.0, progression[0]["average"] - progression[-1]["average"])


def risk_table(
    grades: pd.DataFrame, absences: pd.DataFrame, thresholds: dict
) -> pd.DataFrame:
    """Compute the risk score and segment, one row per student.

    Columns: student_id, average, absence_hours, absence_rate, drop, risk_score, segment.
    """
    if grades.empty:
        return pd.DataFrame(
            columns=[
                "student_id", "average", "absence_hours", "absence_rate",
                "drop", "risk_score", "segment",
            ]
        )

    pass_mark = thresholds["pass_mark"]
    expected_hours = thresholds["expected_hours"]
    high_absence_rate = thresholds["high_absence_rate"]
    drop_thresh = thresholds["performance_drop"]

    abs_hours = (
        absences.groupby("student_id")["hours"].sum()
        if not absences.empty
        else pd.Series(dtype=float)
    )

    records = []
    for sid, g in grades.groupby("student_id"):
        avg = float(g["value"].mean())
        prog = _period_progression(g)
        drop = _drop(prog)
        a_hours = float(abs_hours.get(sid, 0.0))
        a_rate = a_hours / expected_hours if expected_hours else 0.0

        # each component is capped at its fixed weight
        low_avg = max(0.0, (pass_mark - avg) / pass_mark) if avg < pass_mark else 0.0
        score = (
            min(1.0, low_avg) * 50
            + min(1.0, a_rate / high_absence_rate) * 30
            + min(1.0, drop / drop_thresh if drop_thresh else 0) * 20
        )
        score = round(min(100.0, score), 1)
        records.append(
            {
                "student_id": int(sid),
                "average": round(avg, 2),
                "absence_hours": round(a_hours, 1),
                "absence_rate": round(a_rate, 3),
                "drop": round(drop, 2),
                "risk_score": score,
                "segment": segment_for(score, avg, pass_mark),
            }
        )
    return pd.DataFrame(records)


def segment_for(score: float, average: float, pass_mark: float) -> str:
    if score >= 55:
        return "a_risque"
    if score >= 30:
        return "fragile"
    if average >= 16:
        return "excellent"
    if average >= 13:
        return "stable"
    if average >= pass_mark:
        return "moyen"
    return "fragile"


def recommendations(row: dict, thresholds: dict) -> list[str]:
    """Return recommendation codes for a student (rendered to text by the client).

    See ``app.core.messages.RECOMMENDATIONS`` for the FR/EN wording of each code.
    """
    recs: list[str] = []
    if row.get("average", 20) < thresholds["pass_mark"]:
        recs.append("personalized_support")
    if row.get("absence_rate", 0) >= thresholds["high_absence_rate"]:
        recs.append("attendance_reminder")
    if row.get("drop", 0) >= thresholds["performance_drop"]:
        recs.append("analyze_drop")
    if not recs:
        recs.append("stable")
    return recs


def progression_for_student(grades: pd.DataFrame, student_id: int) -> list[dict]:
    g = grades[grades["student_id"] == student_id]
    return _period_progression(g)
