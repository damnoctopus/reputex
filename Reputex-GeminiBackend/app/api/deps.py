"""FastAPI authentication and tenant dependency injection."""
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.models.business import Business
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.business_service import BusinessService


async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
) -> Optional[User]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            return None
        return await AuthService.get_user_by_id(db, user_id)
    except Exception:
        return None


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    user = await get_current_user_optional(authorization, db)
    if not user:
        raise AuthenticationError("Authorization token required")
    return user


async def get_current_business(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_async_db),
) -> Business:
    user_id = current_user.id if current_user else None
    return await BusinessService.get_default_or_first(db, user_id=user_id)
