"""Tests for Phase 5: Dashboard and Analytics endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_and_analytics_flows(client: AsyncClient):
    # 1. Register User with Business
    reg_payload = {
        "email": "analytics_user@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Deepa Analytics",
        "business_name": "Spice Analytics",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Dashboard Summary
    dash_res = await client.get("/api/v1/dashboard", headers=headers)
    assert dash_res.status_code == 200
    d_data = dash_res.json()
    assert "reputation_score" in d_data
    assert "sentiment_distribution" in d_data
    assert "total_mentions" in d_data
    assert "recent_mentions" in d_data

    # 3. Get Dashboard Score
    score_res = await client.get("/api/v1/dashboard/score", headers=headers)
    assert score_res.status_code == 200
    assert "current_score" in score_res.json()

    # 4. Get Sentiment Distribution
    dist_res = await client.get("/api/v1/dashboard/sentiment", headers=headers)
    assert dist_res.status_code == 200
    dist_data = dist_res.json()
    assert "positive" in dist_data
    assert "negative" in dist_data
    assert "total" in dist_data

    # 5. Get Sentiment Trends
    trends_res = await client.get("/api/v1/dashboard/trends?days=7", headers=headers)
    assert trends_res.status_code == 200
    trends = trends_res.json()
    assert isinstance(trends, list)
    assert len(trends) == 7
    assert "date" in trends[0]
    assert "score" in trends[0]

    # 6. Get Platform Breakdown
    plat_res = await client.get("/api/v1/dashboard/platforms", headers=headers)
    assert plat_res.status_code == 200
    plats = plat_res.json()
    assert isinstance(plats, list)
    assert len(plats) > 0
    assert "platform" in plats[0]
    assert "positive_percentage" in plats[0]

    # 7. Test /analytics/ aliases
    analytics_res = await client.get("/api/v1/analytics/sentiment", headers=headers)
    assert analytics_res.status_code == 200
    a_data = analytics_res.json()
    assert "distribution" in a_data
    assert "trends" in a_data
    assert "platform_breakdown" in a_data
