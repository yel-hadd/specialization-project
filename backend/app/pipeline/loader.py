import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Absence, AppClass, Grade, Module, Student


# Les classes, modules et etudiants sont crees a la volee s'ils n'existent pas
# encore, pour pouvoir importer les fichiers dans n'importe quel ordre.
def _get_or_create_class(db: Session, name: str | None, row: dict) -> int | None:
    if not name:
        return None
    cls = db.scalar(select(AppClass).where(AppClass.name == name))
    if cls is None:
        cls = AppClass(
            name=name,
            level=row.get("level"),
            academic_year=row.get("academic_year"),
        )
        db.add(cls)
        db.flush()
    return cls.id


def _get_or_create_module(db: Session, code: str, name: str | None, coef: float) -> int:
    mod = db.scalar(select(Module).where(Module.code == code))
    if mod is None:
        mod = Module(code=code, name=name or code, coefficient=coef or 1.0)
        db.add(mod)
        db.flush()
    return mod.id


def _get_or_create_student(db: Session, code: str, row: dict) -> int:
    st = db.scalar(select(Student).where(Student.student_code == code))
    if st is None:
        st = Student(
            student_code=code,
            first_name=row.get("first_name") or "?",
            last_name=row.get("last_name") or "?",
        )
        db.add(st)
        db.flush()
    return st.id


def load(db: Session, df: pd.DataFrame, dtype: str) -> int:
    """Insere les lignes nettoyees en base. Renvoie le nombre de lignes ecrites."""
    written = 0
    for raw in df.to_dict(orient="records"):
        # pandas met NaN pour les vides, on repasse a None pour la base
        row = {k: (None if pd.isna(v) else v) for k, v in raw.items()}

        if dtype == "students":
            # un import d'etudiants met a jour la fiche si le code existe deja (upsert)
            code = str(row["student_code"])
            st = db.scalar(select(Student).where(Student.student_code == code))
            class_id = _get_or_create_class(db, row.get("class_name"), row)
            if st is None:
                st = Student(student_code=code)
                db.add(st)
            st.first_name = row.get("first_name") or st.first_name or "?"
            st.last_name = row.get("last_name") or st.last_name or "?"
            st.email = row.get("email")
            st.class_id = class_id
            st.enrollment_date = row.get("enrollment_date")
            written += 1

        elif dtype == "grades":
            student_id = _get_or_create_student(db, str(row["student_code"]), row)
            module_id = _get_or_create_module(
                db,
                str(row["module_code"]),
                row.get("module_name"),
                row.get("coefficient") or 1.0,
            )
            db.add(
                Grade(
                    student_id=student_id,
                    module_id=module_id,
                    value=float(row["value"]),
                    assessment_type=row.get("assessment_type"),
                    period=row.get("period"),
                    date=row.get("date"),
                )
            )
            written += 1

        elif dtype == "absences":
            student_id = _get_or_create_student(db, str(row["student_code"]), row)
            module_id = None
            if row.get("module_code"):
                module_id = _get_or_create_module(
                    db, str(row["module_code"]), None, 1.0
                )
            db.add(
                Absence(
                    student_id=student_id,
                    module_id=module_id,
                    date=row.get("date"),
                    hours=float(row.get("hours") or 0.0),
                    type=row.get("type") or "absence",
                    justified=bool(row.get("justified")),
                )
            )
            written += 1

    return written
