"""V1 API Router bundle."""
from fastapi import APIRouter
from app.api.v1.alerts import router as alerts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.business import router as business_router
from app.api.v1.crisis import router as crisis_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.findings import router as findings_router
from app.api.v1.fraud import router as fraud_router
from app.api.v1.issues import router as issues_router
from app.api.v1.keywords import router as keywords_router
from app.api.v1.mentions import router as mentions_router
from app.api.v1.responses import router as responses_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(business_router)
api_v1_router.include_router(keywords_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(mentions_router)
api_v1_router.include_router(issues_router)
api_v1_router.include_router(findings_router)
api_v1_router.include_router(fraud_router)
api_v1_router.include_router(crisis_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(responses_router)
