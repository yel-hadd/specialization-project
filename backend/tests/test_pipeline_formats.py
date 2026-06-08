import io

import pandas as pd
import pytest

from app.models import Grade, ImportLog, Student
from app.pipeline import reader
from app.pipeline.runner import run_import


def _xlsx_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


def test_reader_rejects_unsupported_extension():
    with pytest.raises(ValueError):
        reader.read_file("data.json", b"{}")


def test_excel_import_flow(db):
    students = pd.DataFrame(
        {"student_code": ["S1"], "first_name": ["A"], "last_name": ["B"], "classe": ["C1"]}
    )
    grades = pd.DataFrame(
        {"student_code": ["S1", "S1"], "module": ["M1", "M2"], "note": [14, 9]}
    )

    r1 = run_import(db, "students.xlsx", _xlsx_bytes(students), "students")
    assert r1["status"] == "success"
    r2 = run_import(db, "grades.xlsx", _xlsx_bytes(grades), "auto")  # type detecte automatiquement
    assert r2["status"] == "success"
    assert r2["type"] == "grades"

    assert db.query(Student).count() == 1
    assert db.query(Grade).count() == 2


def test_successful_import_writes_history_row(db):
    students = pd.DataFrame(
        {"student_code": ["S1", "S2"], "first_name": ["A", "C"], "last_name": ["B", "D"]}
    )
    buf = io.StringIO()
    students.to_csv(buf, index=False)
    run_import(db, "students.csv", buf.getvalue().encode(), "students")

    log = db.query(ImportLog).order_by(ImportLog.id.desc()).first()
    assert log is not None
    assert log.filename == "students.csv"
    assert log.rows_processed == 2
    assert log.status == "success"
