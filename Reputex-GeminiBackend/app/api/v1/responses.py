"""AI responses draft and dispatch endpoints matching Flutter Responses repository."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.response import (
    ResponseApproveRequest,
    ResponseDraftResponse,
    ResponseGenerateRequest,
)
from app.services.response_service import ResponseService

router = APIRouter(prefix="/responses", tags=["AI Responses"])


@router.post("/generate", response_model=ResponseDraftResponse)
async def generate_response(
    req: ResponseGenerateRequest,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.generate_response(db, biz.id, req)


@router.get("", response_model=List[ResponseDraftResponse])
async def get_responses(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.get_responses(db, biz.id)


@router.get("/{id}", response_model=ResponseDraftResponse)
async def get_response_by_id(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.get_response_by_id(db, biz.id, id)


@router.post("/{id}/approve", response_model=ResponseDraftResponse)
async def approve_response(
    id: str,
    req: ResponseApproveRequest,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.approve_response(db, biz.id, id, req)


@router.post("/{id}/dispatch", response_model=ResponseDraftResponse)
async def dispatch_response(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.dispatch_response(db, biz.id, id)
