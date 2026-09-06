"""Tests for Phase 4: Intelligence (Sentiment, Aspects, Fraud, Reputation)."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_sentiment_and_aspects(client: AsyncClient):
    # Register user with business
    reg_payload = {
        "email": "intel_user@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Chef Sanjeev",
        "business_name": "Spice Intelligence",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch mentions to get an ID
    m_res = await client.get("/api/v1/mentions", headers=headers)
    assert m_res.status_code == 200
    items = m_res.json()["items"]
    assert len(items) > 0
    mention_id = items[0]["id"]

    # Analyze sentiment
    s_res = await client.post(f"/api/v1/sentiment/analyze/{mention_id}", headers=headers)
    assert s_res.status_code == 200
    s_data = s_res.json()
    assert s_data["sentiment"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert 0.0 <= s_data["confidence"] <= 1.0
    assert "positive_score" in s_data

    # Get aspect analytics
    a_res = await client.get("/api/v1/analytics/aspects", headers=headers)
    assert a_res.status_code == 200
    aspects = a_res.json()
    assert isinstance(aspects, list)
    assert len(aspects) > 0
    assert "aspect" in aspects[0]
    assert "sentiment" in aspects[0]


@pytest.mark.asyncio
async def test_fraud_detection(client: AsyncClient):
    # Register user
    reg_payload = {
        "email": "fraud_test@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Inspector Kumar",
        "business_name": "Spice Fraud Unit",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch mentions
    m_res = await client.get("/api/v1/mentions", headers=headers)
    items = m_res.json()["items"]
    mention_id = items[0]["id"]

    # Get fraud analysis for mention
    f_res = await client.get(f"/api/v1/fraud/{mention_id}", headers=headers)
    assert f_res.status_code == 200
    f_data = f_res.json()
    assert "is_fraudulent" in f_data
    assert "risk_level" in f_data
    assert "reasons" in f_data

    # List all fraud reviews
    flist_res = await client.get("/api/v1/fraud", headers=headers)
    assert flist_res.status_code == 200
    assert isinstance(flist_res.json(), list)


@pytest.mark.asyncio
async def test_reputation_scoring(client: AsyncClient):
    # Register user
    reg_payload = {
        "email": "rep_test@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Manager Priya",
        "business_name": "Spice Reputation",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get reputation score
    rep_res = await client.get("/api/v1/reputation", headers=headers)
    assert rep_res.status_code == 200
    rep_data = rep_res.json()
    assert "current_score" in rep_data
    assert 0.0 <= rep_data["current_score"] <= 100.0
    assert "trend" in rep_data

    # Recalculate reputation score
    recalc_res = await client.post("/api/v1/reputation/recalculate", headers=headers)
    assert recalc_res.status_code == 200
    assert "current_score" in recalc_res.json()

    # Get reputation history
    hist_res = await client.get("/api/v1/reputation/history", headers=headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert isinstance(history, list)
    assert len(history) >= 1
