"""Statistiques descriptives sur les notes (moyenne, mediane, quartiles, etc.)."""

import pandas as pd


def _describe(series: pd.Series) -> dict:
    s = series.dropna()
    if s.empty:
        return {}
    return {
        "count": int(s.count()),
        "mean": round(float(s.mean()), 2),
        "median": round(float(s.median()), 2),
        "min": round(float(s.min()), 2),
        "max": round(float(s.max()), 2),
        "variance": round(float(s.var(ddof=1)) if s.count() > 1 else 0.0, 2),
        "std": round(float(s.std(ddof=1)) if s.count() > 1 else 0.0, 2),
        "q1": round(float(s.quantile(0.25)), 2),
        "q3": round(float(s.quantile(0.75)), 2),
    }


# Stats par module, triees de la plus faible moyenne a la plus haute
# (les modules les plus difficiles ressortent en premier).
def by_module(grades: pd.DataFrame, pass_mark: float) -> list[dict]:
    if grades.empty:
        return []
    out = []
    for (mid, code, name), g in grades.groupby(
        ["module_id", "module_code", "module_name"]
    ):
        stats = _describe(g["value"])
        n = len(g)
        passed = int((g["value"] >= pass_mark).sum())
        stats.update(
            {
                "module_id": int(mid),
                "module_code": code,
                "module_name": name,
                "success_rate": round(passed / n, 3) if n else 0.0,
                "fail_rate": round((n - passed) / n, 3) if n else 0.0,
            }
        )
        out.append(stats)
    return sorted(out, key=lambda d: d.get("mean", 0))


def by_class(grades: pd.DataFrame, pass_mark: float) -> list[dict]:
    if grades.empty or grades["class_id"].isna().all():
        return []
    out = []
    for (cid, name), g in grades.dropna(subset=["class_id"]).groupby(
        ["class_id", "class_name"]
    ):
        stats = _describe(g["value"])
        n = len(g)
        passed = int((g["value"] >= pass_mark).sum())
        stats.update(
            {
                "class_id": int(cid),
                "class_name": name,
                "success_rate": round(passed / n, 3) if n else 0.0,
                "n_students": int(g["student_id"].nunique()),
            }
        )
        out.append(stats)
    return sorted(out, key=lambda d: d.get("mean", 0), reverse=True)


def distribution(grades: pd.DataFrame) -> dict:
    """Histogramme des notes par tranches de 1 point, de 0 a 20."""
    if grades.empty:
        return {"edges": [], "counts": []}
    buckets = pd.cut(grades["value"], bins=range(0, 21), include_lowest=True)
    counts = buckets.value_counts(sort=False)
    edges = [f"{i}-{i + 1}" for i in range(0, 20)]
    return {"edges": edges, "counts": [int(c) for c in counts.values]}
