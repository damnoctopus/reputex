"""AI Response Studio API endpoints matching Flutter RealApiService and OpenAPI specifications."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.ai_response import (
    ApproveResponseRequest,
    GenerateResponseRequest,
    ResponseDraftSchema,
    UpdateResponseRequest,
)
from app.services.ai_service import AIService

router = APIRouter(tags=["AI Response Studio"])


@router.post("/responses/generate", response_model=ResponseDraftSchema, status_code=status.HTTP_201_CREATED)
@router.post("/ai/responses/generate", response_model=ResponseDraftSchema, status_code=status.HTTP_201_CREATED)
async def generate_response(
    req: GenerateResponseRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Generate a calibrated AI response draft for a customer mention."""
    service = AIService(db)
    return await service.generate_response(current_user_id, req)


@router.get("/responses", response_model=list[ResponseDraftSchema])
@router.get("/ai/responses", response_model=list[ResponseDraftSchema])
async def get_responses(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all AI response drafts for the business."""
    service = AIService(db)
    return await service.list_responses(current_user_id)


@router.get("/responses/{id}", response_model=ResponseDraftSchema)
@router.get("/ai/responses/{id}", response_model=ResponseDraftSchema)
async def get_response_by_id(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve details for a single response draft."""
    service = AIService(db)
    return await service.get_response_by_id(current_user_id, id)


@router.put("/responses/{id}", response_model=ResponseDraftSchema)
@router.put("/ai/responses/{id}", response_model=ResponseDraftSchema)
async def update_response(
    id: str,
    req: UpdateResponseRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update or refine the response draft text or tone."""
    service = AIService(db)
    return await service.update_response(current_user_id, id, req)


@router.post("/responses/{id}/approve", response_model=ResponseDraftSchema)
@router.post("/ai/responses/{id}/approve", response_model=ResponseDraftSchema)
async def approve_response(
    id: str,
    req: ApproveResponseRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Approve a response draft with final text."""
    service = AIService(db)
    return await service.approve_response(current_user_id, id, req)


@router.post("/responses/{id}/dispatch", response_model=ResponseDraftSchema)
@router.post("/responses/{id}/publish", response_model=ResponseDraftSchema)
@router.post("/ai/responses/{id}/publish", response_model=ResponseDraftSchema)
async def dispatch_response(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Dispatch/publish an approved response to the target platform."""
    service = AIService(db)
    return await service.dispatch_response(current_user_id, id)
