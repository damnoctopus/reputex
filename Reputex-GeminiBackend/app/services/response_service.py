"""AI customer response drafts and notification alerts service."""
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.gemini_client import GeminiClient
from app.core.exceptions import NotFoundError
from app.models.business import Business
from app.models.mention import Mention
from app.models.response import AlertItem, ResponseDraft
from app.schemas.response import (
    AlertItemResponse,
    ResponseApproveRequest,
    ResponseDraftResponse,
    ResponseGenerateRequest,
)


class ResponseService:
    @staticmethod
    async def generate_response(
        db: AsyncSession,
        business_id: str,
        req: ResponseGenerateRequest,
    ) -> ResponseDraftResponse:
        mention = await db.get(Mention, req.mention_id)
        if not mention:
            raise NotFoundError("Mention", req.mention_id)

        biz = await db.get(Business, business_id)
        biz_name = biz.name if biz else "Business"

        client = GeminiClient()
        text = client.generate_response_draft(
            review_text=mention.content,
            tone=req.tone,
            business_name=biz_name,
            custom_instructions=req.custom_instructions,
        )

        draft = ResponseDraft(
            business_id=business_id,
            mention_id=mention.id,
            response_text=text,
            tone=req.tone,
            status="draft",
        )
        db.add(draft)
        await db.commit()
        await db.refresh(draft)

        return ResponseDraftResponse.model_validate(draft)

    @staticmethod
    async def get_responses(db: AsyncSession, business_id: str) -> List[ResponseDraftResponse]:
        stmt = select(ResponseDraft).where(ResponseDraft.business_id == business_id).order_by(ResponseDraft.created_at.desc())
        res = await db.execute(stmt)
        return [ResponseDraftResponse.model_validate(d) for d in res.scalars().all()]

    @staticmethod
    async def get_response_by_id(db: AsyncSession, business_id: str, response_id: str) -> ResponseDraftResponse:
        stmt = select(ResponseDraft).where(ResponseDraft.id == response_id, ResponseDraft.business_id == business_id)
        res = await db.execute(stmt)
        draft = res.scalar_one_or_none()
        if not draft:
            raise NotFoundError("ResponseDraft", response_id)
        return ResponseDraftResponse.model_validate(draft)

    @staticmethod
    async def approve_response(
        db: AsyncSession,
        business_id: str,
        response_id: str,
        req: ResponseApproveRequest,
    ) -> ResponseDraftResponse:
        stmt = select(ResponseDraft).where(ResponseDraft.id == response_id, ResponseDraft.business_id == business_id)
        res = await db.execute(stmt)
        draft = res.scalar_one_or_none()
        if not draft:
            raise NotFoundError("ResponseDraft", response_id)

        draft.response_text = req.response_text
        draft.status = "approved"
        draft.approved_at = datetime.now(timezone.utc)

        mention = await db.get(Mention, draft.mention_id)
        if mention:
            mention.response_status = "approved"
            mention.response_text = req.response_text

        await db.commit()
        await db.refresh(draft)
        return ResponseDraftResponse.model_validate(draft)

    @staticmethod
    async def dispatch_response(
        db: AsyncSession,
        business_id: str,
        response_id: str,
    ) -> ResponseDraftResponse:
        stmt = select(ResponseDraft).where(ResponseDraft.id == response_id, ResponseDraft.business_id == business_id)
        res = await db.execute(stmt)
        draft = res.scalar_one_or_none()
        if not draft:
            raise NotFoundError("ResponseDraft", response_id)

        draft.status = "dispatched"
        draft.dispatched_at = datetime.now(timezone.utc)

        mention = await db.get(Mention, draft.mention_id)
        if mention:
            mention.response_status = "dispatched"

        await db.commit()
        await db.refresh(draft)
        return ResponseDraftResponse.model_validate(draft)

    @staticmethod
    async def get_alerts(db: AsyncSession, business_id: str) -> List[AlertItemResponse]:
        stmt = select(AlertItem).where(AlertItem.business_id == business_id).order_by(AlertItem.created_at.desc())
        res = await db.execute(stmt)
        alerts = list(res.scalars().all())
        if not alerts:
            default_alert = AlertItem(
                business_id=business_id,
                title="RepuTex Intelligence Active",
                message="Monitoring Google, Reddit, and X mentions with automated anomaly detection.",
                severity="low",
                alert_type="system",
            )
            db.add(default_alert)
            await db.commit()
            await db.refresh(default_alert)
            alerts = [default_alert]

        return [
            AlertItemResponse(
                id=str(a.id),
                business_id=str(a.business_id),
                title=a.title,
                message=a.message,
                severity=a.severity or "medium",
                type=a.alert_type or "system",
                alert_type=a.alert_type or "system",
                is_read=a.is_read,
                timestamp=a.created_at,
                created_at=a.created_at,
                metadata_json=a.metadata_json or {},
            )
            for a in alerts
        ]

    @staticmethod
    async def mark_alert_as_read(db: AsyncSession, business_id: str, alert_id: str) -> None:
        stmt = select(AlertItem).where(AlertItem.id == alert_id, AlertItem.business_id == business_id)
        res = await db.execute(stmt)
        alert = res.scalar_one_or_none()
        if alert:
            alert.is_read = True
            await db.commit()
