"""Comprehensive end-to-end integration test validating Flutter RealApiService contract over /api base."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_flutter_real_api_service_full_contract(client: AsyncClient):
    # ── 1. Authentication (/api/auth/...) ──
    reg_payload = {
        "email": "flutter_dev@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Flutter Integrator",
        "business_name": "Spice Flutter Branch",
        "business_category": "Fine Dining",
    }
    reg_res = await client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    auth_data = reg_res.json()
    assert "user" in auth_data
    assert "tokens" in auth_data
    access_token = auth_data["tokens"]["access_token"]
    refresh_token = auth_data["tokens"]["refresh_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Login
    login_res = await client.post(
        "/api/auth/login",
        json={"email": "flutter_dev@spicesymphony.com", "password": "SecurePassword123!"},
    )
    assert login_res.status_code == 200

    # Refresh token
    ref_res = await client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert ref_res.status_code == 200
    assert "access_token" in ref_res.json()

    # Get current user (/api/auth/me)
    me_res = await client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "flutter_dev@spicesymphony.com"

    # ── 2. Business & Keywords (/api/business, /api/keywords) ──
    biz_res = await client.get("/api/business", headers=headers)
    assert biz_res.status_code == 200
    assert biz_res.json()["name"] == "Spice Flutter Branch"

    kw_post = await client.post(
        "/api/keywords",
        json={"keyword": "tandoori chicken", "category": "product"},
        headers=headers,
    )
    assert kw_post.status_code == 201
    kw_id = kw_post.json()["id"]

    kw_list = await client.get("/api/keywords", headers=headers)
    assert kw_list.status_code == 200
    assert any(k["id"] == kw_id for k in kw_list.json())

    # ── 3. Dashboard & Analytics (/api/dashboard, /api/analytics/sentiment) ──
    dash_res = await client.get("/api/dashboard", headers=headers)
    assert dash_res.status_code == 200
    d = dash_res.json()
    assert "reputation_score" in d
    assert "sentiment_distribution" in d
    assert "total_mentions" in d
    assert "recent_mentions" in d

    score_res = await client.get("/api/dashboard/score", headers=headers)
    assert score_res.status_code == 200
    assert "current_score" in score_res.json()

    dist_res = await client.get("/api/dashboard/sentiment", headers=headers)
    assert dist_res.status_code == 200
    assert "positive_percentage" in dist_res.json()

    trends_res = await client.get("/api/dashboard/trends?days=7", headers=headers)
    assert trends_res.status_code == 200
    assert len(trends_res.json()) == 7

    plats_res = await client.get("/api/dashboard/platforms", headers=headers)
    assert plats_res.status_code == 200
    assert len(plats_res.json()) > 0

    analytics_res = await client.get("/api/analytics/sentiment", headers=headers)
    assert analytics_res.status_code == 200
    assert "platform_breakdown" in analytics_res.json()

    # ── 4. Mentions (/api/mentions) ──
    post_m = await client.post(
        "/api/mentions",
        json={"platform": "Google", "author": "FlutterFan", "content": "Superb dining experience!", "rating": 5.0},
        headers=headers,
    )
    assert post_m.status_code == 201

    m_res = await client.get(
        "/api/mentions",
        params={"page": 1, "limit": 10, "sort_by": "newest"},
        headers=headers,
    )
    assert m_res.status_code == 200
    m_data = m_res.json()
    assert "items" in m_data
    assert len(m_data["items"]) > 0
    mention = m_data["items"][0]
    mention_id = mention["id"]
    # Check timestamp field mapping specifically for Flutter
    assert "timestamp" in mention

    m_single = await client.get(f"/api/mentions/{mention_id}", headers=headers)
    assert m_single.status_code == 200
    assert m_single.json()["id"] == mention_id

    # ── 5. Fraud Detection (/api/fraud) ──
    fraud_list = await client.get("/api/fraud", headers=headers)
    assert fraud_list.status_code == 200
    assert isinstance(fraud_list.json(), list)

    fraud_single = await client.get(f"/api/fraud/{mention_id}", headers=headers)
    assert fraud_single.status_code == 200
    assert "is_fraudulent" in fraud_single.json()
    assert "reasons" in fraud_single.json()

    # ── 6. Crisis Monitoring (/api/crisis) ──
    crisis_list = await client.get("/api/crisis", headers=headers)
    assert crisis_list.status_code == 200
    crisis_events = crisis_list.json()
    assert len(crisis_events) > 0
    crisis_id = crisis_events[0]["id"]

    crisis_active = await client.get("/api/crisis/active", headers=headers)
    assert crisis_active.status_code == 200

    crisis_single = await client.get(f"/api/crisis/{crisis_id}", headers=headers)
    assert crisis_single.status_code == 200
    assert crisis_single.json()["id"] == crisis_id

    # ── 7. Alerts (/api/alerts) ──
    alerts_res = await client.get("/api/alerts", headers=headers)
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert len(alerts) > 0
    alert_id = alerts[0]["id"]
    assert "timestamp" in alerts[0]

    # Flutter RealApiService calls PUT /api/alerts/{id}/read
    put_read = await client.put(f"/api/alerts/{alert_id}/read", headers=headers)
    assert put_read.status_code == 200

    # ── 8. AI Responses (/api/responses) ──
    gen_res = await client.post(
        "/api/responses/generate",
        json={"mention_id": mention_id, "tone": "empathetic"},
        headers=headers,
    )
    assert gen_res.status_code == 201
    draft_id = gen_res.json()["id"]

    resp_list = await client.get("/api/responses", headers=headers)
    assert resp_list.status_code == 200
    assert any(r["id"] == draft_id for r in resp_list.json())

    resp_single = await client.get(f"/api/responses/{draft_id}", headers=headers)
    assert resp_single.status_code == 200
    assert resp_single.json()["id"] == draft_id

    approve_res = await client.post(
        f"/api/responses/{draft_id}/approve",
        json={"response_text": "Approved response text."},
        headers=headers,
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "approved"

    dispatch_res = await client.post(f"/api/responses/{draft_id}/dispatch", headers=headers)
    assert dispatch_res.status_code == 200
    assert dispatch_res.json()["status"] == "dispatched"

    # ── 9. Devices Push Notification (/api/devices/register) ──
    device_res = await client.post("/api/devices/register", headers=headers)
    assert device_res.status_code == 200
    assert device_res.json()["success"] is True
