"""Brand keywords API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.business import BrandKeywordCreate, BrandKeywordSchema
from app.services.business_service import BusinessService

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.get(
    "",
    response_model=list[BrandKeywordSchema],
    status_code=status.HTTP_200_OK,
    summary="List all tracked keywords for active business",
)
async def list_keywords(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.list_keywords(current_user_id)


@router.post(
    "",
    response_model=BrandKeywordSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add brand keyword for active business",
)
async def add_keyword(
    req: BrandKeywordCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.add_keyword(current_user_id, req)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete brand keyword by ID",
)
async def delete_keyword(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    await service.delete_keyword(current_user_id, id)
