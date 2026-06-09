"""Correlation entre absences, retards et resultats."""

import pandas as pd


def student_feature_table(
    grades: pd.DataFrame, absences: pd.DataFrame
) -> pd.DataFrame:
    """Par etudiant : moyenne, heures d'absence et heures de retard."""
    if grades.empty:
        return pd.DataFrame()

    avg = grades.groupby("student_id")["value"].mean().rename("average")
    std = grades.groupby("student_id")["value"].std(ddof=1).rename("grade_std")

    if absences.empty:
        abs_hours = pd.Series(dtype=float, name="absence_hours")
        late_hours = pd.Series(dtype=float, name="lateness_hours")
    else:
        abs_hours = (
            absences[absences["type"] == "absence"]
            .groupby("student_id")["hours"]
            .sum()
            .rename("absence_hours")
        )
        late_hours = (
            absences[absences["type"] == "retard"]
            .groupby("student_id")["hours"]
            .sum()
            .rename("lateness_hours")
        )

    table = pd.concat([avg, std, abs_hours, late_hours], axis=1)
    table = table.fillna({"absence_hours": 0.0, "lateness_hours": 0.0, "grade_std": 0.0})
    # concat perd le nom de l'index quand les series d'absences sont vides ;
    # on le remet pour que le reste du code retrouve bien "student_id".
    table.index.name = "student_id"
    return table.dropna(subset=["average"])


def correlation_matrix(table: pd.DataFrame) -> dict:
    """Matrice de correlation de Pearson, en dict pret a afficher en heatmap."""
    cols = ["average", "grade_std", "absence_hours", "lateness_hours"]
    cols = [c for c in cols if c in table.columns]
    if table.empty or len(table) < 2:
        return {"labels": cols, "matrix": []}
    corr = table[cols].corr(method="pearson").round(3).fillna(0.0)
    return {
        "labels": cols,
        "matrix": corr.values.tolist(),
    }
