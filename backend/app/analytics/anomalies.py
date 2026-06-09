"""Detection d'anomalies : notes inhabituelles et absences excessives."""

import pandas as pd


def grade_outliers(grades: pd.DataFrame, z_thresh: float = 2.5) -> list[dict]:
    """Signale les notes loin de la moyenne de leur module (via le z-score)."""
    if grades.empty:
        return []
    out = []
    for mid, g in grades.groupby("module_id"):
        # en dessous de 3 notes le z-score n'a pas de sens, on passe
        if len(g) < 3:
            continue
        mean = g["value"].mean()
        std = g["value"].std(ddof=1)
        if not std or pd.isna(std):
            continue
        g = g.assign(z=(g["value"] - mean) / std)
        flagged = g[g["z"].abs() >= z_thresh]
        for _, r in flagged.iterrows():
            out.append(
                {
                    "student_id": int(r["student_id"]),
                    "student_code": r["student_code"],
                    "module_name": r["module_name"],
                    "value": round(float(r["value"]), 2),
                    "module_mean": round(float(mean), 2),
                    "z_score": round(float(r["z"]), 2),
                }
            )
    return out


def absence_outliers(absences: pd.DataFrame, iqr_factor: float = 1.5) -> list[dict]:
    """Signale les etudiants dont le total d'heures d'absence depasse la borne IQR."""
    if absences.empty:
        return []
    totals = absences.groupby(["student_id", "student_code"])["hours"].sum()
    if len(totals) < 4:
        return []
    q1, q3 = totals.quantile(0.25), totals.quantile(0.75)
    fence = q3 + iqr_factor * (q3 - q1)
    flagged = totals[totals > fence]
    return [
        {"student_id": int(sid), "student_code": code, "absence_hours": round(float(h), 1)}
        for (sid, code), h in flagged.items()
    ]
