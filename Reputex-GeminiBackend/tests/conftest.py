"""Pytest test configuration and shared fixtures."""
import os
import sys
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

backend_root = r"c:\Users\adira\Projects\major\Reputex-GeminiBackend"
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.core.database import get_async_db
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.services.business_service import BusinessService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def clean_db_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def test_business(db_session: AsyncSession) -> Business:
    return await BusinessService.get_default_or_first(db_session)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_async_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()
