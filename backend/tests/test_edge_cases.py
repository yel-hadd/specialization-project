import io

import pandas as pd

from app.analytics import service
from app.models import ImportLog
from app.pipeline.runner import run_import


def _csv(df: pd.DataFrame) -> bytes:
    b = io.StringIO()
    df.to_csv(b, index=False)
    return b.getvalue().encode()


def test_kpis_on_empty_database(db):
    k = service.kpis(db)
    assert k["n_students"] == 0
    assert k["n_grades"] == 0
    assert k["overall_average"] is None
    assert k["n_at_risk"] == 0


def test_empty_database_analytics_are_safe(db):
    assert service.module_analysis(db) == []
    assert service.class_analysis(db) == []
    assert service.at_risk_students(db) == []
    assert service.segmentation_summary(db) == {"counts": {}, "students": []}
    assert service.grade_distribution(db) == {"edges": [], "counts": []}


def test_import_with_all_invalid_rows(db):
    # Fichier de notes ou chaque ligne n'a pas la valeur obligatoire.
    grades = pd.DataFrame(
        {"student_code": ["S1", "S2"], "module": ["M1", "M2"], "note": [None, None]}
    )
    res = run_import(db, "g.csv", _csv(grades), "grades")
    assert res["rows_processed"] == 0
    assert res["rows_rejected"] == 2
    assert res["status"] == "partial"

    log = db.query(ImportLog).order_by(ImportLog.id.desc()).first()
    assert log.rows_rejected == 2


def test_student_detail_missing_returns_none(db):
    assert service.student_detail(db, 9999) is None
