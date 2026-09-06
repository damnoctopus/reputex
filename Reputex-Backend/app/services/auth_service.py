"""Authentication domain service handling user registration, login, and token issuance."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.business import Business, BusinessMember
from app.models.user import User
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AuthResponseSchema,
    AuthTokensSchema,
    LoginRequest,
    RegisterRequest,
    UserSchema,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.business_repo = BusinessRepository(db)

    async def register(self, req: RegisterRequest) -> AuthResponseSchema:
        # Check if email is already registered
        existing_user = await self.user_repo.get_by_email(req.email)
        if existing_user:
            raise ConflictException(
                message="An account with this email address already exists.",
                code="EMAIL_ALREADY_EXISTS",
            )

        # 1. Create User
        user = User(
            email=req.email.strip().lower(),
            password_hash=hash_password(req.password),
            full_name=req.full_name.strip(),
            phone=req.phone,
            role="owner",
            is_active=True,
        )
        self.db.add(user)
        await self.db.flush()

        # 2. Create Initial Business
        business = Business(
            owner_id=user.id,
            name=req.business_name.strip(),
            category=req.business_category,
            phone=req.phone,
            monitored_platforms=["Google", "JustDial", "Reddit", "X"],
        )
        self.db.add(business)
        await self.db.flush()

        # 3. Associate user with business and create membership
        user.business_id = business.id
        member = BusinessMember(
            business_id=business.id,
            user_id=user.id,
            role="owner",
        )
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(user)

        # 4. Generate Tokens
        access_token = create_access_token(
            subject=user.id,
            business_id=business.id,
            role=user.role,
        )
        refresh_token = create_refresh_token(subject=user.id)

        return AuthResponseSchema(
            user=UserSchema.model_validate(user),
            tokens=AuthTokensSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=3600,
            ),
        )

    async def login(self, req: LoginRequest) -> AuthResponseSchema:
        user = await self.user_repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise UnauthorizedException(
                message="Invalid email or password.",
                code="INVALID_CREDENTIALS",
            )

        if not user.is_active:
            raise UnauthorizedException(
                message="Your account has been deactivated. Please contact support.",
                code="ACCOUNT_DEACTIVATED",
            )

        access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )
        refresh_token = create_refresh_token(subject=user.id)

        return AuthResponseSchema(
            user=UserSchema.model_validate(user),
            tokens=AuthTokensSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=3600,
            ),
        )

    async def refresh_token(self, token_str: str) -> AuthTokensSchema:
        payload = decode_token(token_str)
        if payload.get("type") != "refresh":
            raise UnauthorizedException(
                message="Invalid token type. Expected refresh token.",
                code="INVALID_TOKEN_TYPE",
            )

        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(
                message="User session not found or deactivated.",
                code="USER_NOT_FOUND",
            )

        new_access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )
        new_refresh_token = create_refresh_token(subject=user.id)

        return AuthTokensSchema(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=3600,
        )

    async def get_current_user(self, user_id: str) -> UserSchema:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(
                message="User profile not found.",
                code="USER_NOT_FOUND",
            )
        return UserSchema.model_validate(user)
