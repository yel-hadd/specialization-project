"""Load database records into pandas DataFrames for analysis."""

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Absence, AppClass, Grade, Module, Student


def grades_frame(db: Session) -> pd.DataFrame:
    """One row per grade, joined with student, class, and module fields."""
    rows = db.execute(
        select(
            Grade.id,
            Grade.value,
            Grade.period,
            Grade.assessment_type,
            Grade.date,
            Student.id.label("student_id"),
            Student.student_code,
            Student.first_name,
            Student.last_name,
            AppClass.id.label("class_id"),
            AppClass.name.label("class_name"),
            Module.id.label("module_id"),
            Module.code.label("module_code"),
            Module.name.label("module_name"),
            Module.coefficient,
        )
        .join(Student, Grade.student_id == Student.id)
        .join(Module, Grade.module_id == Module.id)
        .join(AppClass, Student.class_id == AppClass.id, isouter=True)
    ).all()
    return pd.DataFrame(rows, columns=[
        "id", "value", "period", "assessment_type", "date", "student_id",
        "student_code", "first_name", "last_name", "class_id", "class_name",
        "module_id", "module_code", "module_name", "coefficient",
    ])


def absences_frame(db: Session) -> pd.DataFrame:
    """One row per absence, joined with the student and class."""
    rows = db.execute(
        select(
            Absence.id,
            Absence.hours,
            Absence.type,
            Absence.justified,
            Absence.date,
            Student.id.label("student_id"),
            Student.student_code,
            AppClass.id.label("class_id"),
            AppClass.name.label("class_name"),
        )
        .join(Student, Absence.student_id == Student.id)
        .join(AppClass, Student.class_id == AppClass.id, isouter=True)
    ).all()
    return pd.DataFrame(rows, columns=[
        "id", "hours", "type", "justified", "date", "student_id",
        "student_code", "class_id", "class_name",
    ])


def students_frame(db: Session) -> pd.DataFrame:
    rows = db.execute(
        select(
            Student.id,
            Student.student_code,
            Student.first_name,
            Student.last_name,
            Student.email,
            AppClass.id.label("class_id"),
            AppClass.name.label("class_name"),
        ).join(AppClass, Student.class_id == AppClass.id, isouter=True)
    ).all()
    return pd.DataFrame(rows, columns=[
        "id", "student_code", "first_name", "last_name", "email",
        "class_id", "class_name",
    ])
