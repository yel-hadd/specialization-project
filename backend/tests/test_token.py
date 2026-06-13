from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token


def test_token_roundtrip():
    token = create_access_token("user@edu.io")
    assert decode_access_token(token) == "user@edu.io"


def test_garbage_token_returns_none():
    assert decode_access_token("not-a-real-token") is None


def test_expired_token_returns_none():
    # Build an already-expired token.
    payload = {
        "sub": "user@edu.io",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    expired = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    assert decode_access_token(expired) is None


def test_token_signed_with_wrong_secret_returns_none():
    payload = {
        "sub": "user@edu.io",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
    }
    forged = jwt.encode(payload, "wrong-secret", algorithm=settings.jwt_algorithm)
    assert decode_access_token(forged) is None
