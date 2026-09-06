"""Business and Keyword repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.business import BrandKeyword, Business, BusinessMember
from app.repositories.base import BaseRepository


class BusinessRepository(BaseRepository[Business]):
    def __init__(self, db: AsyncSession):
        super().__init__(Business, db)

    async def get_by_id_with_keywords(self, business_id: str) -> Business | None:
        result = await self.db.execute(
            select(Business).where(Business.id == business_id).options(selectinload(Business.keywords))
        )
        return result.scalars().first()

    async def list_by_owner(self, owner_id: str) -> list[Business]:
        result = await self.db.execute(
            select(Business).where(Business.owner_id == owner_id).options(selectinload(Business.keywords))
        )
        return list(result.scalars().all())

    async def get_user_member_record(self, business_id: str, user_id: str) -> BusinessMember | None:
        result = await self.db.execute(
            select(BusinessMember).where(
                BusinessMember.business_id == business_id,
                BusinessMember.user_id == user_id,
            )
        )
        return result.scalars().first()

    async def add_member(self, business_id: str, user_id: str, role: str = "owner") -> BusinessMember:
        member = BusinessMember(business_id=business_id, user_id=user_id, role=role)
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    # Brand Keywords operations
    async def list_keywords(self, business_id: str) -> list[BrandKeyword]:
        result = await self.db.execute(
            select(BrandKeyword).where(BrandKeyword.business_id == business_id).order_by(BrandKeyword.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_keyword_by_id(self, keyword_id: str) -> BrandKeyword | None:
        result = await self.db.execute(select(BrandKeyword).where(BrandKeyword.id == keyword_id))
        return result.scalars().first()

    async def add_keyword(self, business_id: str, keyword: str, category: str = "brand") -> BrandKeyword:
        kw = BrandKeyword(business_id=business_id, keyword=keyword, category=category)
        self.db.add(kw)
        await self.db.commit()
        await self.db.refresh(kw)
        return kw

    async def delete_keyword(self, kw: BrandKeyword) -> None:
        await self.db.delete(kw)
        await self.db.commit()
