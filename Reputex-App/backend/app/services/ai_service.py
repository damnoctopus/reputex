"""AI Response Studio domain service."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.provider import get_ai_provider
from app.core.exceptions import NotFoundException
from app.models.ai_response import AIResponse
from app.models.mention import Mention
from app.repositories.business_repository import BusinessRepository
from app.repositories.mention_repository import MentionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ai_response import (
    ApproveResponseRequest,
    GenerateResponseRequest,
    ResponseDraftSchema,
    UpdateResponseRequest,
)


class AIService:
    """Manages AI-assisted response generation, tone calibration, review approval, and dispatch."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_provider = get_ai_provider()
        self.user_repo = UserRepository(db)
        self.business_repo = BusinessRepository(db)
        self.mention_repo = MentionRepository(db)

    async def _resolve_business_id(self, user_id: str) -> str:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            businesses = await self.business_repo.list_by_owner(user_id)
            if businesses:
                return businesses[0].id
            raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")
        return user.business_id

    async def generate_response(self, user_id: str, req: GenerateResponseRequest) -> ResponseDraftSchema:
        business_id = await self._resolve_business_id(user_id)
        mention = await self.mention_repo.get_by_business_and_id(business_id, req.mention_id)
        if not mention:
            raise NotFoundException("Mention not found", code="MENTION_NOT_FOUND")

        business = await self.business_repo.get_by_id(business_id)
        biz_name = business.name if business else "Our Business"

        # Generate response via AI Provider
        draft_text = await self.ai_provider.generate_response(
            review_text=mention.content,
            tone=req.tone,
            business_name=biz_name,
            custom_instructions=req.custom_instructions,
        )

        response_draft = AIResponse(
            business_id=business_id,
            mention_id=mention.id,
            original_review=mention.content,
            generated_response=draft_text,
            tone=req.tone,
            status="drafted",
            created_at=datetime.now(UTC),
        )
        self.db.add(response_draft)
        await self.db.commit()
        await self.db.refresh(response_draft)

        return ResponseDraftSchema.model_validate(response_draft)

    async def list_responses(self, user_id: str) -> list[ResponseDraftSchema]:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(AIResponse).where(AIResponse.business_id == business_id).order_by(AIResponse.created_at.desc())
        drafts = list((await self.db.execute(stmt)).scalars().all())

        if not drafts:
            drafts = await self._seed_default_responses(business_id)

        return [ResponseDraftSchema.model_validate(d) for d in drafts]

    async def get_response_by_id(self, user_id: str, response_id: str) -> ResponseDraftSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(AIResponse).where(
            AIResponse.business_id == business_id,
            AIResponse.id == response_id,
        )
        draft = (await self.db.execute(stmt)).scalars().first()
        if not draft:
            raise NotFoundException("Response draft not found", code="RESPONSE_NOT_FOUND")
        return ResponseDraftSchema.model_validate(draft)

    async def update_response(self, user_id: str, response_id: str, req: UpdateResponseRequest) -> ResponseDraftSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(AIResponse).where(
            AIResponse.business_id == business_id,
            AIResponse.id == response_id,
        )
        draft = (await self.db.execute(stmt)).scalars().first()
        if not draft:
            raise NotFoundException("Response draft not found", code="RESPONSE_NOT_FOUND")

        if req.response_text:
            draft.generated_response = req.response_text
        if req.tone:
            draft.tone = req.tone

        await self.db.commit()
        await self.db.refresh(draft)
        return ResponseDraftSchema.model_validate(draft)

    async def approve_response(
        self, user_id: str, response_id: str, req: ApproveResponseRequest
    ) -> ResponseDraftSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(AIResponse).where(
            AIResponse.business_id == business_id,
            AIResponse.id == response_id,
        )
        draft = (await self.db.execute(stmt)).scalars().first()
        if not draft:
            raise NotFoundException("Response draft not found", code="RESPONSE_NOT_FOUND")

        if req.response_text:
            draft.generated_response = req.response_text
        draft.status = "approved"
        draft.approved_at = datetime.now(UTC)

        await self.db.commit()
        await self.db.refresh(draft)
        return ResponseDraftSchema.model_validate(draft)

    async def dispatch_response(self, user_id: str, response_id: str) -> ResponseDraftSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(AIResponse).where(
            AIResponse.business_id == business_id,
            AIResponse.id == response_id,
        )
        draft = (await self.db.execute(stmt)).scalars().first()
        if not draft:
            raise NotFoundException("Response draft not found", code="RESPONSE_NOT_FOUND")

        draft.status = "dispatched"
        draft.dispatched_at = datetime.now(UTC)

        await self.db.commit()
        await self.db.refresh(draft)
        return ResponseDraftSchema.model_validate(draft)

    async def _seed_default_responses(self, business_id: str) -> list[AIResponse]:
        # Find negative mentions to attach response drafts
        stmt = select(Mention).where(Mention.business_id == business_id).limit(3)
        mentions = list((await self.db.execute(stmt)).scalars().all())
        if not mentions:
            return []

        seeded = []
        for m in mentions:
            draft = AIResponse(
                business_id=business_id,
                mention_id=m.id,
                original_review=m.content,
                generated_response=(
                    f"Thank you for sharing your feedback on {m.platform}. We take your experience seriously "
                    "and will continue refining our dining quality. Please reach out so we can host you again."
                ),
                tone="empathetic",
                status="drafted",
                created_at=datetime.now(UTC),
            )
            self.db.add(draft)
            seeded.append(draft)

        await self.db.commit()
        for d in seeded:
            await self.db.refresh(d)
        return seeded
