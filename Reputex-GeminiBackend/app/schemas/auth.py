"""Authentication schemas matching Flutter AuthResponse and User models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    business_name: str
    business_category: str = "General"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    role: str = "owner"
    business_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: AuthTokens
