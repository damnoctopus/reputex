"""Tests for Phase 5: Alerts endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_alerts_lifecycle(client: AsyncClient):
    # 1. Register User with Business
    reg_payload = {
        "email": "alerts_lead@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Alert Officer Ananya",
        "business_name": "Spice Alerts",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Alerts (seeds default alerts)
    alerts_res = await client.get("/api/v1/alerts", headers=headers)
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert isinstance(alerts, list)
    assert len(alerts) > 0
    first_alert = alerts[0]
    assert "type" in first_alert
    assert "title" in first_alert
    assert "timestamp" in first_alert

    # 3. Mark Single Alert Read via PUT (Flutter client style)
    alert_id = first_alert["id"]
    put_res = await client.put(f"/api/v1/alerts/{alert_id}/read", headers=headers)
    assert put_res.status_code == 200
    assert put_res.json()["success"] is True

    # 4. Mark All Alerts Read via PATCH
    all_read_res = await client.patch("/api/v1/alerts/read-all", headers=headers)
    assert all_read_res.status_code == 200
    assert all_read_res.json()["success"] is True

    # Verify all are read
    refreshed_alerts = (await client.get("/api/v1/alerts", headers=headers)).json()
    assert all(a["is_read"] is True for a in refreshed_alerts)
