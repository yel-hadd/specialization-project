import io

import pandas as pd

from app.analytics import service
from app.pipeline.runner import run_import


def _seed(db):
    """Import a small but structured dataset: classes, modules, periods."""
    students = pd.DataFrame(
        {
            "student_code": [f"S{i}" for i in range(1, 13)],
            "first_name": [f"F{i}" for i in range(1, 13)],
            "last_name": [f"L{i}" for i in range(1, 13)],
            "classe": ["C1"] * 6 + ["C2"] * 6,
        }
    )
    rows = []
    for i in range(1, 13):
        base = 5 if i <= 4 else 12 if i <= 8 else 17  # low, average, strong cohorts
        for mod in ["M1", "M2"]:
            for period, delta in [("S1", 0), ("S2", -1)]:
                rows.append(
                    {
                        "student_code": f"S{i}",
                        "module": mod,
                        "note": max(0, min(20, base + delta)),
                        "periode": period,
                    }
                )
    grades = pd.DataFrame(rows)
    absences = pd.DataFrame(
        {
            "student_code": [f"S{i}" for i in range(1, 5)],
            "date": ["2025-09-15"] * 4,
            "heures": [40, 35, 30, 25],
            "type_absence": ["absence"] * 4,
        }
    )

    def csv(df):
        b = io.StringIO()
        df.to_csv(b, index=False)
        return b.getvalue().encode()

    run_import(db, "students.csv", csv(students), "students")
    run_import(db, "grades.csv", csv(grades), "grades")
    run_import(db, "absences.csv", csv(absences), "absences")


def test_kpis_computed_from_data(db):
    _seed(db)
    k = service.kpis(db)
    assert k["n_students"] == 12
    assert k["n_grades"] == 48
    assert 0 <= k["success_rate"] <= 1
    assert k["overall_average"] is not None
    assert k["n_at_risk"] >= 1  # the low cohort


def test_module_and_class_analysis(db):
    _seed(db)
    modules = service.module_analysis(db)
    assert len(modules) == 2
    assert all("success_rate" in m for m in modules)

    classes = service.class_analysis(db)
    assert {c["class_name"] for c in classes} == {"C1", "C2"}


def test_correlations_and_segmentation(db):
    _seed(db)
    corr = service.correlations(db)
    assert "average" in corr["labels"]
    assert len(corr["matrix"]) == len(corr["labels"])

    seg = service.segmentation_summary(db)
    assert sum(seg["counts"].values()) == 12


def test_student_detail_has_rank_and_progression(db):
    _seed(db)
    detail = service.student_detail(db, 1)
    assert detail is not None
    assert detail["rank"] is not None
    assert detail["class_size"] == 6
    assert len(detail["progression"]) == 2  # S1 and S2
    assert detail["recommendations"]
