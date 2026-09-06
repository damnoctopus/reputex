"""Integration tests for Scan, Issues, Findings, and extended Dashboard APIs."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_scan_issues_and_findings_workflow(client: AsyncClient):
    # 1. Register User and Business
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "scan_owner@spicesymphony.com",
            "password": "Password123!",
            "full_name": "Scan Owner",
            "business_name": "Spice Symphony",
            "business_category": "Restaurant",
        },
    )
    assert reg_res.status_code == 201
    token = reg_res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get active business ID
    biz_res = await client.get("/api/v1/business", headers=headers)
    assert biz_res.status_code == 200
    biz_id = biz_res.json()["id"]

    # 3. Trigger Full Scan
    scan_res = await client.post(f"/api/v1/businesses/{biz_id}/scan", headers=headers)
    assert scan_res.status_code == 202
    scan_data = scan_res.json()
    assert scan_data["business_id"] == biz_id

    # 4. Check Scan Status
    status_res = await client.get(f"/api/v1/businesses/{biz_id}/scan/status", headers=headers)
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert status_data["business_id"] == biz_id
    assert "active_platforms" in status_data

    # 5. Check Issues API
    issues_res = await client.get(f"/api/v1/businesses/{biz_id}/issues", headers=headers)
    assert issues_res.status_code == 200
    issues_data = issues_res.json()
    assert "items" in issues_data
    assert "total_count" in issues_data

    # 6. Check Findings API
    findings_res = await client.get(f"/api/v1/businesses/{biz_id}/findings", headers=headers)
    assert findings_res.status_code == 200
    findings_data = findings_res.json()
    assert "items" in findings_data
    assert "total_count" in findings_data

    # 7. Check Suspicious Reviews API
    suspicious_res = await client.get(f"/api/v1/businesses/{biz_id}/suspicious-reviews", headers=headers)
    assert suspicious_res.status_code == 200
    suspicious_data = suspicious_res.json()
    assert "items" in suspicious_data

    # 8. Check Dashboard Summary has top_issues and crisis_risk_level
    dash_res = await client.get("/api/v1/dashboard/summary", headers=headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert "top_issues" in dash_data
    assert "crisis_risk_level" in dash_data
    assert "suspicious_reviews_count" in dash_data
    assert "active_clusters_count" in dash_data
