"""Business profile and keywords management service."""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError
from app.models.business import BrandKeyword, Business
from app.schemas.business import (
    BrandKeywordCreate,
    BrandKeywordResponse,
    BusinessResponse,
    BusinessSetupRequest,
)


class BusinessService:
    @staticmethod
    async def get_business_by_id(db: AsyncSession, business_id: str) -> Business:
        stmt = select(Business).where(Business.id == business_id).options(selectinload(Business.keywords))
        result = await db.execute(stmt)
        biz = result.scalar_one_or_none()
        if not biz:
            raise NotFoundError("Business", business_id)
        return biz

    @staticmethod
    async def get_default_or_first(db: AsyncSession, user_id: Optional[str] = None) -> Business:
        if user_id:
            stmt = select(Business).where(Business.owner_id == user_id).options(selectinload(Business.keywords)).limit(1)
            res = await db.execute(stmt)
            biz = res.scalars().first()
            if biz:
                return biz

        stmt = select(Business).options(selectinload(Business.keywords)).limit(1)
        res = await db.execute(stmt)
        biz = res.scalars().first()
        if not biz:
            biz = Business(
                name="Spice Symphony",
                category="Restaurant",
                location="Downtown",
                monitored_platforms=["google", "reddit", "twitter"],
            )
            db.add(biz)
            await db.flush()
            for kw in ["Spice Symphony", "Spice Symphony food", "Spice Symphony reviews"]:
                db.add(BrandKeyword(business_id=biz.id, keyword=kw, category="brand"))
            await db.commit()
            await db.refresh(biz, ["keywords"])
        return biz

    @staticmethod
    async def setup_business(
        db: AsyncSession,
        user_id: Optional[str],
        req: BusinessSetupRequest,
    ) -> Business:
        biz = Business(
            name=req.name,
            category=req.category,
            website=req.website,
            location=req.location,
            phone=req.phone,
            monitored_platforms=req.platforms or ["google", "reddit", "twitter"],
            owner_id=user_id,
        )
        db.add(biz)
        await db.flush()

        for kw in req.keywords:
            if kw.strip():
                db.add(BrandKeyword(business_id=biz.id, keyword=kw.strip(), category="brand"))

        await db.commit()
        return await BusinessService.get_business_by_id(db, biz.id)

    @staticmethod
    async def add_keyword(db: AsyncSession, business_id: str, req: BrandKeywordCreate) -> BrandKeyword:
        kw = BrandKeyword(
            business_id=business_id,
            keyword=req.keyword.strip(),
            category=req.category,
        )
        db.add(kw)
        await db.commit()
        await db.refresh(kw)
        return kw

    @staticmethod
    async def get_keywords(db: AsyncSession, business_id: str) -> List[BrandKeyword]:
        stmt = select(BrandKeyword).where(BrandKeyword.business_id == business_id).order_by(BrandKeyword.created_at.desc())
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def delete_keyword(db: AsyncSession, business_id: str, keyword_id: str) -> None:
        stmt = select(BrandKeyword).where(BrandKeyword.id == keyword_id, BrandKeyword.business_id == business_id)
        res = await db.execute(stmt)
        kw = res.scalar_one_or_none()
        if kw:
            await db.delete(kw)
            await db.commit()
