import io
import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as database


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestSession = sessionmaker(bind=engine)
    database.engine = engine
    database.SessionLocal = TestSession

    from app.core.database import Base, get_db
    import app.models  # noqa: F401

    Base.metadata.create_all(engine)
    from app.main import app

    def override_get_db():
        s = TestSession()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _auth(client) -> dict:
    client.post("/auth/register", json={"email": "u@e.l", "password": "secret123"})
    token = client.post(
        "/auth/login", data={"username": "u@e.l", "password": "secret123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_garbage_token_rejected(client):
    r = client.get("/analytics/kpis", headers={"Authorization": "Bearer not.a.jwt"})
    assert r.status_code == 401


def test_duplicate_email_rejected(client):
    client.post("/auth/register", json={"email": "dup@e.l", "password": "x12345678"})
    r = client.post("/auth/register", json={"email": "dup@e.l", "password": "x12345678"})
    assert r.status_code == 400


def test_all_data_routers_require_auth(client):
    for path in ["/students", "/classes", "/modules", "/imports", "/alerts"]:
        assert client.get(path).status_code == 401, path


def test_import_unsupported_type_via_api(client):
    headers = _auth(client)
    files = {"file": ("data.json", b"{}", "application/json")}
    r = client.post("/imports", files=files, data={"type": "auto"}, headers=headers)
    # The pipeline records a failed import instead of raising a 500.
    assert r.status_code == 200
    assert r.json()["status"] == "failed"


def test_alert_generation_flow(client):
    headers = _auth(client)
    students = pd.DataFrame(
        {"student_code": ["S1", "S2"], "first_name": ["A", "C"], "last_name": ["B", "D"]}
    )
    grades = pd.DataFrame(
        {"student_code": ["S1", "S2"], "module": ["M1", "M1"], "note": [4, 18]}
    )

    def csv(df):
        b = io.StringIO()
        df.to_csv(b, index=False)
        return b.getvalue().encode()

    client.post("/imports", files={"file": ("s.csv", csv(students))}, data={"type": "students"}, headers=headers)
    client.post("/imports", files={"file": ("g.csv", csv(grades))}, data={"type": "grades"}, headers=headers)

    gen = client.post("/alerts/generate", headers=headers)
    assert gen.status_code == 200
    assert gen.json()["created"] >= 1  # the failing student triggers a low_average alert

    alerts = client.get("/alerts", headers=headers).json()
    assert any(a["alert_type"] == "low_average" for a in alerts)


def test_report_html_endpoint(client):
    headers = _auth(client)
    r = client.get("/reports/html", headers=headers)
    assert r.status_code == 200
    assert "EduTrack" in r.text
