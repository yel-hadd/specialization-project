import io

import pandas as pd

from app.analytics import service
from app.models import Grade, Student
from app.pipeline.runner import run_import


def _csv_bytes(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode()


def test_full_import_flow(db):
    students = pd.DataFrame(
        {
            "student_code": ["S1", "S2"],
            "first_name": ["A", "B"],
            "last_name": ["X", "Y"],
            "classe": ["C1", "C1"],
        }
    )
    grades = pd.DataFrame(
        {
            "student_code": ["S1", "S2", "S1"],
            "module": ["M1", "M1", "M2"],
            "note": [12, 8, 15],
            "periode": ["S1", "S1", "S1"],
        }
    )

    r1 = run_import(db, "students.csv", _csv_bytes(students), "students")
    assert r1["status"] == "success"
    assert r1["rows_processed"] == 2

    r2 = run_import(db, "grades.csv", _csv_bytes(grades), "grades")
    assert r2["status"] == "success"
    assert r2["rows_processed"] == 3

    assert db.query(Student).count() == 2
    assert db.query(Grade).count() == 3

    kpis = service.kpis(db)
    assert kpis["n_students"] == 2
    assert kpis["n_grades"] == 3
    assert kpis["overall_average"] is not None


def test_failed_import_records_log(db):
    bad = pd.DataFrame({"foo": [1], "bar": [2]})
    res = run_import(db, "bad.csv", _csv_bytes(bad), "grades")
    assert res["status"] == "failed"
    assert res["errors"]
