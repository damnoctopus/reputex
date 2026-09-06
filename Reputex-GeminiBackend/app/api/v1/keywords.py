"""Brand keywords endpoints matching Flutter BusinessRepository."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.business import BrandKeywordCreate, BrandKeywordResponse
from app.services.business_service import BusinessService

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.get("", response_model=List[BrandKeywordResponse])
async def get_keywords(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    keywords = await BusinessService.get_keywords(db, biz.id)
    return [BrandKeywordResponse.model_validate(k) for k in keywords]


@router.post("", response_model=BrandKeywordResponse, status_code=status.HTTP_201_CREATED)
async def add_keyword(
    req: BrandKeywordCreate,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    kw = await BusinessService.add_keyword(db, biz.id, req)
    return BrandKeywordResponse.model_validate(kw)


@router.delete("/{id}")
async def delete_keyword(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    await BusinessService.delete_keyword(db, biz.id, id)
    return {"message": "Keyword deleted successfully"}
