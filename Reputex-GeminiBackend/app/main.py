"""FastAPI Main Application entrypoint."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1 import api_v1_router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, async_engine
from app.core.exceptions import ReputexException
from app.models.base import Base
from app.services.business_service import BusinessService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("reputex")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    logger.info("Initializing database schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Ensure default demo business exists
    async with AsyncSessionLocal() as db:
        await BusinessService.get_default_or_first(db)

    logger.info("RepuTex Backend initialized successfully.")
    yield
    # Shutdown
    await async_engine.dispose()
    logger.info("RepuTex Backend shutdown completed.")


app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Clean, high-performance RepuTex intelligence backend with Gemini Search Grounding.",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler matching Flutter ErrorHandler
@app.exception_handler(ReputexException)
async def reputex_exception_handler(request: Request, exc: ReputexException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred.",
            "detail": str(exc),
        },
    )


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "gemini_model": settings.GEMINI_MODEL,
        "mock_acquisition": settings.USE_MOCK_ACQUISITION,
        "mock_gemini": settings.USE_MOCK_GEMINI,
    }


# Mount API routers at BOTH /api (Flutter's default baseUrl) AND /api/v1 (REST standards)
app.include_router(api_v1_router, prefix="/api")
app.include_router(api_v1_router, prefix="/api/v1")
