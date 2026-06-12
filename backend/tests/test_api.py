import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as database


@pytest.fixture()
def client():
    """TestClient adosse a une base SQLite en memoire neuve."""
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
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_protected_route_requires_token(client):
    assert client.get("/analytics/kpis").status_code == 401


def test_register_login_and_access(client):
    # Cree un utilisateur.
    r = client.post(
        "/auth/register",
        json={"email": "teacher@edu.io", "password": "secret123"},
    )
    assert r.status_code == 201

    # Connexion via le formulaire mot de passe OAuth2.
    r = client.post(
        "/auth/login",
        data={"username": "teacher@edu.io", "password": "secret123"},
    )
    assert r.status_code == 200
    token = r.json()["access_token"]

    # Accede a une route protegee avec le token.
    r = client.get("/analytics/kpis", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert "n_students" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "a@b.c", "password": "rightpass"})
    r = client.post("/auth/login", data={"username": "a@b.c", "password": "wrongpass"})
    assert r.status_code == 401
