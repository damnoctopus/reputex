"""FastAPI dependency injection utilities for authentication, authorization, and tenant isolation."""

from typing import Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)
from app.core.security import decode_token

security_scheme = HTTPBearer(auto_error=False)


async def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> dict[str, Any]:
    """Extract and validate JWT Bearer token from request headers."""
    if not credentials or not credentials.credentials:
        raise UnauthorizedException(
            message="Authentication required. Missing Bearer token.",
            code="UNAUTHORIZED",
        )
    return decode_token(credentials.credentials)


async def get_current_user_id(
    payload: dict[str, Any] = Depends(get_token_payload),
) -> str:
    """Extract authenticated user ID (subject) from token."""
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException(
            message="Invalid token subject.",
            code="INVALID_TOKEN",
        )
    return str(user_id)


def require_roles(allowed_roles: list[str]):
    """Role-based authorization dependency factory."""

    async def role_checker(payload: dict[str, Any] = Depends(get_token_payload)) -> dict[str, Any]:
        user_role = str(payload.get("role", "viewer")).lower()
        normalized_allowed = [r.lower() for r in allowed_roles]
        if user_role not in normalized_allowed:
            raise ForbiddenException(
                message=f"Access forbidden. Required role: {', '.join(allowed_roles)}.",
                code="INSUFFICIENT_PERMISSIONS",
            )
        return payload

    return role_checker


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve full User entity from authenticated token subject."""
    from app.repositories.user_repository import UserRepository

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise UnauthorizedException(
            message="User account not found or deactivated.",
            code="USER_NOT_FOUND",
        )
    return user
