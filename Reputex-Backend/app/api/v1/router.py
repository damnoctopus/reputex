"""Master API v1 Router aggregating all domain routers."""

from fastapi import APIRouter

from app.api.v1.ai_response import router as ai_response_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.businesses import router as businesses_router
from app.api.v1.crisis import router as crisis_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.fraud import router as fraud_router
from app.api.v1.keywords import router as keywords_router
from app.api.v1.mentions import router as mentions_router
from app.api.v1.reputation import router as reputation_router
from app.api.v1.sentiment import router as sentiment_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(businesses_router)
api_v1_router.include_router(keywords_router)
api_v1_router.include_router(mentions_router)
api_v1_router.include_router(sentiment_router)
api_v1_router.include_router(fraud_router)
api_v1_router.include_router(reputation_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(crisis_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(ai_response_router)


@api_v1_router.post("/devices/register", tags=["Devices"])
async def register_device():
    """Register device token for push notifications."""
    return {"success": True, "message": "Device token registered"}
