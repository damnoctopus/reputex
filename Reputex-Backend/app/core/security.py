"""Security utilities: Argon2id password hashing and PyJWT token management."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# Initialize Argon2 password hasher with memory-hard parameters
_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64 MB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return _hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its Argon2id hash."""
    try:
        return _hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_access_token(
    subject: str,
    business_id: str | None = None,
    role: str = "owner",
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(UTC)
    expire = now + expires_delta if expires_delta else now + timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_MINUTES)

    payload: dict[str, Any] = {
        "sub": subject,
        "business_id": business_id,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT refresh token."""
    now = datetime.now(UTC)
    expire = now + expires_delta if expires_delta else now + timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token signature and expiration."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(
            message="Token has expired. Please log in again.",
            code="TOKEN_EXPIRED",
        )
    except jwt.InvalidTokenError:
        raise UnauthorizedException(
            message="Invalid authentication token.",
            code="INVALID_TOKEN",
        )
