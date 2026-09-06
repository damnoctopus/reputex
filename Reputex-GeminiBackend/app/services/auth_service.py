"""Authentication and user registration service."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.business import Business
from app.models.user import User
from app.schemas.auth import AuthResponse, AuthTokens, LoginRequest, RegisterRequest, UserResponse


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, req: RegisterRequest) -> AuthResponse:
        # Check existing user
        result = await db.execute(select(User).where(User.email == req.email.lower()))
        if result.scalar_one_or_none():
            raise ConflictError(f"User with email '{req.email}' already exists")

        # Create business
        biz = Business(
            name=req.business_name,
            category=req.business_category,
            monitored_platforms=["google", "reddit", "twitter"],
        )
        db.add(biz)
        await db.flush()

        # Create user
        user = User(
            email=req.email.lower(),
            password_hash=get_password_hash(req.password),
            full_name=req.full_name,
            business_id=biz.id,
        )
        db.add(user)
        await db.flush()

        biz.owner_id = user.id
        await db.commit()
        await db.refresh(user)

        tokens = AuthTokens(
            access_token=create_access_token(user.id, {"business_id": user.business_id, "role": user.role}),
            refresh_token=create_refresh_token(user.id),
        )
        return AuthResponse(user=UserResponse.model_validate(user), tokens=tokens)

    @staticmethod
    async def login(db: AsyncSession, req: LoginRequest) -> AuthResponse:
        result = await db.execute(select(User).where(User.email == req.email.lower()))
        user = result.scalar_one_or_none()
        if not user or not verify_password(req.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")

        tokens = AuthTokens(
            access_token=create_access_token(user.id, {"business_id": user.business_id, "role": user.role}),
            refresh_token=create_refresh_token(user.id),
        )
        return AuthResponse(user=UserResponse.model_validate(user), tokens=tokens)

    @staticmethod
    async def refresh_token(db: AsyncSession, token_str: str) -> AuthTokens:
        try:
            payload = decode_token(token_str)
            if payload.get("type") != "refresh":
                raise AuthenticationError("Invalid token type")
            user_id = payload.get("sub")
        except Exception:
            raise AuthenticationError("Token expired or invalid")

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")

        return AuthTokens(
            access_token=create_access_token(user.id, {"business_id": user.business_id, "role": user.role}),
            refresh_token=create_refresh_token(user.id),
        )

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User", user_id)
        return user
