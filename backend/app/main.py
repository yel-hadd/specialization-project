import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.routers import (
    alerts,
    analytics,
    auth,
    catalog,
    imports,
    reports,
    students,
)
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Setting, User


def _seed(db) -> None:
    """Create the default admin and seed the adjustable thresholds (once)."""
    if not db.scalar(select(User).where(User.email == settings.admin_email)):
        db.add(
            User(
                email=settings.admin_email,
                hashed_password=hash_password(settings.admin_password),
                role="admin",
            )
        )
    defaults = {
        "pass_mark": settings.pass_mark,
        "high_absence_rate": settings.high_absence_rate,
        "performance_drop": settings.performance_drop,
        "expected_hours": settings.expected_hours,
    }
    existing = {s.key for s in db.scalars(select(Setting)).all()}
    for key, value in defaults.items():
        if key not in existing:
            db.add(Setting(key=key, value=value))
    db.commit()


def _check_secrets() -> None:
    """Warn loudly when the app is running with the shipped default credentials."""
    if settings.jwt_secret == "change-me-in-production":
        logging.warning(
            "JWT_SECRET is still the default value; set a strong secret via the "
            "JWT_SECRET environment variable before deploying."
        )
    if settings.admin_password == "admin123":
        logging.warning(
            "ADMIN_PASSWORD is still the default value; change it before deploying."
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _check_secrets()
    db = SessionLocal()
    try:
        _seed(db)
    finally:
        db.close()
    yield


app = FastAPI(title="EduTrack Analytics API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(imports.router)
app.include_router(students.router)
app.include_router(catalog.router)
app.include_router(analytics.router)
app.include_router(alerts.router)
app.include_router(reports.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
