"""Smoke test local : lance le pipeline et les analytics sur une base SQLite en memoire.

Outil de developpement, pas inclus dans l'app deployee. A lancer depuis backend/ :
    DATABASE_URL=sqlite:// python smoke_test.py
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

from pathlib import Path  # noqa: E402

from sqlalchemy import StaticPool, create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

import app.core.database as database  # noqa: E402

# Une seule connexion en memoire partagee pour tout le test.
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
database.engine = engine
database.SessionLocal = sessionmaker(bind=engine)

from app.core.database import Base  # noqa: E402
import app.models  # noqa: E402,F401

Base.metadata.create_all(engine)

from app.analytics import service  # noqa: E402
from app.pipeline.runner import run_import  # noqa: E402

SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"


def main() -> None:
    db = database.SessionLocal()

    for name, dtype in [
        ("etudiants.csv", "students"),
        ("notes.csv", "grades"),
        ("absences.xlsx", "absences"),
    ]:
        content = (SAMPLES / name).read_bytes()
        res = run_import(db, name, content, dtype)
        print(f"import {name}: status={res['status']} "
              f"processed={res['rows_processed']} rejected={res['rows_rejected']} "
              f"warnings={len(res['warnings'])}")

    print("\nKPIs:", service.kpis(db))
    print("\nModules (top 2 hardest):")
    for m in service.module_analysis(db)[:2]:
        print(f"  {m['module_name']}: mean={m['mean']} success={m['success_rate']}")
    print("\nClasses:")
    for c in service.class_analysis(db):
        print(f"  {c['class_name']}: mean={c['mean']}")
    corr = service.correlations(db)
    print("\nCorrelation labels:", corr["labels"])
    print("Correlation matrix rows:", len(corr["matrix"]))
    seg = service.segmentation_summary(db)
    print("\nSegmentation:", seg["counts"])
    at_risk = service.at_risk_students(db)
    print(f"\nAt-risk students: {len(at_risk)}")
    if at_risk:
        print("  example:", at_risk[0]["name"], "score", at_risk[0]["risk_score"])
    detail = service.student_detail(db, 1)
    print("\nStudent #1 detail: average=", detail["average"],
          "segment=", detail["risk_segment"], "rank=", detail["rank"])
    print("  progression points:", len(detail["progression"]))
    print("\nSMOKE TEST OK")


if __name__ == "__main__":
    main()
