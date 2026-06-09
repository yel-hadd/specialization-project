"""Score de risque (a base de regles) et segmentation des etudiants.

Le score (0 a 100) combine trois signaux :
  - moyenne faible par rapport au seuil de validation
  - taux d'absence eleve par rapport au volume horaire attendu
  - baisse de performance entre la premiere et la derniere periode
Le score donne ensuite un segment : excellent, stable, moyen, fragile, a_risque.
"""

import pandas as pd


def _period_progression(g: pd.DataFrame) -> list[dict]:
    """Moyenne par periode, dans l'ordre, pour les notes d'un etudiant."""
    if g.empty or g["period"].isna().all():
        return []
    prog = (
        g.dropna(subset=["period"])
        .groupby("period")["value"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("period")
    )
    return [{"period": r["period"], "average": float(r["value"])} for _, r in prog.iterrows()]


def _drop(progression: list[dict]) -> float:
    """Points perdus entre la premiere et la derniere periode (0 si en progres)."""
    if len(progression) < 2:
        return 0.0
    return max(0.0, progression[0]["average"] - progression[-1]["average"])


def risk_table(
    grades: pd.DataFrame, absences: pd.DataFrame, thresholds: dict
) -> pd.DataFrame:
    """Score de risque et segment, un par etudiant.

    Colonnes : student_id, average, absence_hours, absence_rate, drop, risk_score, segment.
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

        # chaque composante est plafonnee a son poids fixe
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
    """Actions pedagogiques en clair pour un etudiant."""
    recs: list[str] = []
    if row.get("average", 20) < thresholds["pass_mark"]:
        recs.append("Mettre en place un suivi personnalise et un soutien sur les modules faibles.")
    if row.get("absence_rate", 0) >= thresholds["high_absence_rate"]:
        recs.append("Envoyer un rappel d'assiduite et contacter l'etudiant.")
    if row.get("drop", 0) >= thresholds["performance_drop"]:
        recs.append("Analyser la baisse recente de performance et proposer un point individuel.")
    if not recs:
        recs.append("Situation stable, poursuivre le suivi habituel.")
    return recs


def progression_for_student(grades: pd.DataFrame, student_id: int) -> list[dict]:
    g = grades[grades["student_id"] == student_id]
    return _period_progression(g)
