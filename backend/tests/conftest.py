import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as database


@pytest.fixture()
def db():
    """Provide an isolated in-memory SQLite session for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(bind=engine)

    # Point the app's session factory at the test engine.
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
