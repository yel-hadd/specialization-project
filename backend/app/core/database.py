from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Classe de base pour tous les modeles ORM."""


def get_db() -> Generator[Session, None, None]:
    """Dependance FastAPI qui fournit une session de base de donnees."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
