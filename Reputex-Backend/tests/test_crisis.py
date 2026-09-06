"""Tests for Phase 5: Crisis Monitoring endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_crisis_monitoring_flows(client: AsyncClient):
    # 1. Register User with Business
    reg_payload = {
        "email": "crisis_officer@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Crisis Lead Vikram",
        "business_name": "Spice Crisis Unit",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Crisis Events (seeds default crisis)
    events_res = await client.get("/api/v1/crisis", headers=headers)
    assert events_res.status_code == 200
    events = events_res.json()
    assert isinstance(events, list)
    assert len(events) > 0
    crisis_id = events[0]["id"]
    assert "severity" in events[0]
    assert "trigger_reason" in events[0]

    # 3. Get Active Crisis
    active_res = await client.get("/api/v1/crisis/active", headers=headers)
    assert active_res.status_code == 200
    active = active_res.json()
    assert active is not None
    assert active["status"] == "active"

    # 4. Get Crisis by ID
    single_res = await client.get(f"/api/v1/crisis/{crisis_id}", headers=headers)
    assert single_res.status_code == 200
    assert single_res.json()["id"] == crisis_id

    # 5. Patch Crisis (Resolve crisis)
    patch_res = await client.patch(
        f"/api/v1/crisis/{crisis_id}",
        json={"status": "resolved"},
        headers=headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "resolved"
    assert patch_res.json()["resolved_at"] is not None

    # 6. Trigger Crisis Analyze
    analyze_res = await client.post("/api/v1/crisis/analyze", headers=headers)
    assert analyze_res.status_code == 200
