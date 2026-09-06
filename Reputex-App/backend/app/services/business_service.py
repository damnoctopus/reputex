"""Business and Keywords domain service with multi-tenant authorization."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.models.business import BrandKeyword, Business
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.business import (
    BrandKeywordCreate,
    BrandKeywordSchema,
    BusinessSchema,
    BusinessSetupRequest,
    BusinessUpdateRequest,
)


class BusinessService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.user_repo = UserRepository(db)

    async def verify_business_access(self, user_id: str, business_id: str) -> Business:
        """Enforces tenant isolation: verifies that user is owner or active member of business."""
        business = await self.business_repo.get_by_id_with_keywords(business_id)
        if not business:
            raise NotFoundException(
                message="Business profile not found.",
                code="BUSINESS_NOT_FOUND",
            )

        # Check direct ownership
        if business.owner_id == user_id:
            return business

        # Check membership
        member = await self.business_repo.get_user_member_record(business_id, user_id)
        if not member:
            raise ForbiddenException(
                message="Access denied. You are not a member of this business.",
                code="BUSINESS_ACCESS_DENIED",
            )
        return business

    async def get_active_business(self, user_id: str) -> BusinessSchema | None:
        """Fetch the active business for the user."""
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            # Check if user owns any business
            businesses = await self.business_repo.list_by_owner(user_id)
            if businesses:
                return BusinessSchema.model_validate(businesses[0])
            return None

        business = await self.business_repo.get_by_id_with_keywords(user.business_id)
        if not business:
            return None
        return BusinessSchema.model_validate(business)

    async def setup_business(self, user_id: str, req: BusinessSetupRequest) -> BusinessSchema:
        """Onboarding wizard setup: creates or updates business with platforms and keywords."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found", code="USER_NOT_FOUND")

        business = None
        if user.business_id:
            business = await self.business_repo.get_by_id_with_keywords(user.business_id)

        if not business:
            business = Business(
                owner_id=user_id,
                name=req.name,
                category=req.category,
                website=req.website,
                location=req.location,
                phone=req.phone,
                monitored_platforms=req.platforms or ["Google", "JustDial", "Reddit", "X"],
            )
            self.db.add(business)
            await self.db.flush()
            user.business_id = business.id
            await self.business_repo.add_member(business.id, user_id, role="owner")
        else:
            business.name = req.name
            business.category = req.category
            if req.website is not None:
                business.website = req.website
            if req.location is not None:
                business.location = req.location
            if req.phone is not None:
                business.phone = req.phone
            if req.platforms:
                business.monitored_platforms = req.platforms

        # Add brand keywords
        existing_keywords = {kw.keyword.lower() for kw in await self.business_repo.list_keywords(business.id)}
        for kw_str in req.keywords:
            clean_kw = kw_str.strip()
            if clean_kw and clean_kw.lower() not in existing_keywords:
                kw_model = BrandKeyword(business_id=business.id, keyword=clean_kw, category="brand")
                self.db.add(kw_model)

        await self.db.commit()
        await self.db.refresh(business, ["keywords"])
        return BusinessSchema.model_validate(business)

    async def list_businesses(self, user_id: str) -> list[BusinessSchema]:
        businesses = await self.business_repo.list_by_owner(user_id)
        return [BusinessSchema.model_validate(b) for b in businesses]

    async def get_business_by_id(self, user_id: str, business_id: str) -> BusinessSchema:
        business = await self.verify_business_access(user_id, business_id)
        return BusinessSchema.model_validate(business)

    async def update_business(self, user_id: str, business_id: str, req: BusinessUpdateRequest) -> BusinessSchema:
        business = await self.verify_business_access(user_id, business_id)
        if req.name is not None:
            business.name = req.name
        if req.category is not None:
            business.category = req.category
        if req.description is not None:
            business.description = req.description
        if req.website is not None:
            business.website = req.website
        if req.location is not None:
            business.location = req.location
        if req.phone is not None:
            business.phone = req.phone
        if req.monitored_platforms is not None:
            business.monitored_platforms = req.monitored_platforms

        await self.db.commit()
        await self.db.refresh(business)
        return BusinessSchema.model_validate(business)

    async def delete_business(self, user_id: str, business_id: str) -> None:
        business = await self.verify_business_access(user_id, business_id)
        if business.owner_id != user_id:
            raise ForbiddenException(
                "Only the business owner can delete this business.", code="OWNER_PERMISSION_REQUIRED"
            )
        await self.business_repo.delete(business)

    # Keyword management
    async def list_keywords(self, user_id: str) -> list[BrandKeywordSchema]:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            return []
        keywords = await self.business_repo.list_keywords(user.business_id)
        return [BrandKeywordSchema.model_validate(kw) for kw in keywords]

    async def add_keyword(self, user_id: str, req: BrandKeywordCreate) -> BrandKeywordSchema:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            raise NotFoundException("Active business not found for user", code="BUSINESS_NOT_FOUND")

        kw = await self.business_repo.add_keyword(
            business_id=user.business_id,
            keyword=req.keyword.strip(),
            category=req.category,
        )
        return BrandKeywordSchema.model_validate(kw)

    async def delete_keyword(self, user_id: str, keyword_id: str) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")

        kw = await self.business_repo.get_keyword_by_id(keyword_id)
        if not kw or kw.business_id != user.business_id:
            raise NotFoundException("Keyword not found", code="KEYWORD_NOT_FOUND")

        await self.business_repo.delete_keyword(kw)
