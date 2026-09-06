"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.auth import (
    AuthResponseSchema,
    AuthTokensSchema,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    UserSchema,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account and initialize default business",
)
async def register(
    req: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.register(req)


@router.post(
    "/login",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Log in with email and password",
)
async def login(
    req: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(req)


@router.post(
    "/refresh",
    response_model=AuthTokensSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token using refresh token",
)
async def refresh_token(
    req: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.refresh_token(req.refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Log out and invalidate session",
)
async def logout(
    current_user_id: str = Depends(get_current_user_id),
):
    return {"success": True, "message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get profile of the currently authenticated user",
)
async def get_me(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.get_current_user(current_user_id)
