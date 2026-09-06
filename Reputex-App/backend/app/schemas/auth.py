"""Authentication Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role: str = "owner"
    business_id: str | None = None
    is_active: bool = True
    created_at: datetime | None = None


class AuthTokensSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int | None = 3600


class AuthResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserSchema
    tokens: AuthTokensSchema


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, description="Plaintext password minimum 6 chars")
    full_name: str = Field(min_length=1)
    business_name: str = Field(min_length=1)
    business_category: str = Field(default="Restaurant")
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
