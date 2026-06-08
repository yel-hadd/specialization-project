import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as database


@pytest.fixture()
def db():
    """Une session SQLite en memoire isolee pour chaque test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(bind=engine)

    # Pointe la fabrique de sessions de l'app vers le moteur de test.
    database.engine = engine
    database.SessionLocal = TestSession

    from app.core.database import Base
    import app.models  # noqa: F401

    Base.metadata.create_all(engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
