"""Authentication endpoints matching Flutter AuthRepository."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_async_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    AuthTokens,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    return await AuthService.register(db, req)


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    return await AuthService.login(db, req)


@router.post("/refresh", response_model=AuthTokens)
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_async_db)):
    return await AuthService.refresh_token(db, req.refresh_token)


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
