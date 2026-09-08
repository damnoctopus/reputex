"""Global pytest test fixtures and test environment setup."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app

# In-memory SQLite async test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
async def setup_test_db():
    """Create all tables before each test and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_test_db) -> AsyncGenerator[AsyncSession, None]:
    """Provide isolated async session for database tests."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an asynchronous HTTP client configured with test DB override."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_async_session_local(monkeypatch):
    """Ensure background tasks use the test in-memory database."""
    monkeypatch.setattr("app.workers.tasks.AsyncSessionLocal", TestAsyncSessionLocal)


@pytest.fixture(autouse=True)
def mock_fire_and_forget_tasks(monkeypatch):
    """Prevent fire-and-forget background tasks from running in tests (like Celery mock did)."""
    async def mock_coro(*args, **kwargs):
        pass

    from app.workers import tasks

    for task_name in [
        "pipeline_process_mentions",
        "ingest_platform_for_business",
        "fetch_mentions",
        "process_sentiment",
        "analyze_fraud",
        "calculate_reputation",
        "detect_crisis",
        "generate_alerts",
    ]:
        monkeypatch.setattr(tasks, task_name, mock_coro)
