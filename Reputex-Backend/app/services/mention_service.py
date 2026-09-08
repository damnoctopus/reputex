"""Mentions and Reviews domain service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.mention import Mention
from app.repositories.business_repository import BusinessRepository
from app.repositories.mention_repository import MentionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.mention import (
    MentionCreateRequest,
    MentionSchema,
    MentionsFilterParams,
    PaginatedMentionsSchema,
)


class MentionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.mention_repo = MentionRepository(db)
        self.user_repo = UserRepository(db)
        self.business_repo = BusinessRepository(db)

    async def _resolve_business_id(self, user_id: str) -> str:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            businesses = await self.business_repo.list_by_owner(user_id)
            if businesses:
                return businesses[0].id
            raise NotFoundException("No active business found for user.", code="BUSINESS_NOT_FOUND")
        return user.business_id

    async def get_paginated_mentions(
        self,
        user_id: str,
        filter_params: MentionsFilterParams,
        reviews_only: bool = False,
    ) -> PaginatedMentionsSchema:
        business_id = await self._resolve_business_id(user_id)

        items, total_count, total_pages, has_more = await self.mention_repo.list_paginated(
            business_id=business_id,
            filter_params=filter_params,
            reviews_only=reviews_only,
        )

        return PaginatedMentionsSchema(
            items=[MentionSchema.model_validate(m) for m in items],
            total_count=total_count,
            page=filter_params.page,
            total_pages=total_pages,
            has_more=has_more,
        )

    async def get_mention_by_id(self, user_id: str, mention_id: str) -> MentionSchema:
        business_id = await self._resolve_business_id(user_id)
        mention = await self.mention_repo.get_by_business_and_id(business_id, mention_id)
        if not mention:
            raise NotFoundException("Mention not found.", code="MENTION_NOT_FOUND")
        return MentionSchema.model_validate(mention)

    async def create_mention(self, user_id: str, req: MentionCreateRequest) -> MentionSchema:
        business_id = await self._resolve_business_id(user_id)
        mention = Mention(
            business_id=business_id,
            platform=req.platform,
            author=req.author,
            content=req.content,
            rating=req.rating,
            url=req.url,
            sentiment=req.sentiment,
            sentiment_score=req.sentiment_score,
            is_fake=req.is_fake,
            fraud_confidence=req.fraud_confidence,
            engagement=req.engagement,
            author_avatar=req.author_avatar,
        )
        if req.published_at:
            mention.published_at = req.published_at
        created = await self.mention_repo.create(mention)
        return MentionSchema.model_validate(created)
