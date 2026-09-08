import asyncio
import pytest
from httpx import AsyncClient

from app.workers.tasks import scan_business_full


@pytest.mark.asyncio
async def test_concurrent_scan_execution(client: AsyncClient):
    """
    Ensure that triggering multiple scans concurrently does not exhaust or break the connection pool.
    Previously, using Celery's `asyncio.run(coro)` in thread pools caused SQLAlchemy Queue 
    event-loop binding issues and leaked connections.
    """
    # 1. Register User and Business
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "concurrent_scan@example.com",
            "password": "Password123!",
            "full_name": "Concurrent Owner",
            "business_name": "Concurrent Business",
            "business_category": "Retail",
        },
    )
    assert reg_res.status_code == 201
    token = reg_res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get active business ID
    biz_res = await client.get("/api/v1/business", headers=headers)
    assert biz_res.status_code == 200
    biz_id = biz_res.json()["id"]

    # 3. Pre-create platform connections to avoid SQLite concurrent INSERT locking issues during the test
    from app.core.database import AsyncSessionLocal
    from app.repositories.platform_repository import PlatformConnectionRepository
    async with AsyncSessionLocal() as session:
        repo = PlatformConnectionRepository(session)
        for p in ["google", "reddit", "twitter"]:
            await repo.get_or_create(biz_id, p)

    # 4. Trigger multiple scans concurrently to simulate heavy load
    # By calling scan_business_full concurrently in the same event loop, 
    # we verify that SQLAlchemy's async engine connection pool can safely 
    # check out and return connections without throwing "Queue is bound to a different event loop"
    tasks = [scan_business_full(biz_id) for _ in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 4. Verify all scans completed without exceptions (like RuntimeError from the pool)
    for res in results:
        assert isinstance(res, dict)
        assert res.get("status") == "completed", f"Scan failed or returned error: {res}"

    # 5. Verify the app can still connect to the DB after the scans
    status_res = await client.get(f"/api/v1/businesses/{biz_id}/scan/status", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["business_id"] == biz_id
