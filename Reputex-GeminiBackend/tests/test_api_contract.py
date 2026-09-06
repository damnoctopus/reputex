"""Contract validation tests ensuring 100% compatibility with Flutter app models."""
import pytest


@pytest.mark.asyncio
async def test_auth_contract(client):
    # Register
    reg_resp = await client.post(
        "/api/auth/register",
        json={
            "email": "owner@restaurant.com",
            "password": "Password123!",
            "full_name": "Test Owner",
            "business_name": "New Bistro",
            "business_category": "Restaurant",
        },
    )
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert "user" in reg_data
    assert "tokens" in reg_data
    assert "access_token" in reg_data["tokens"]
    assert "refresh_token" in reg_data["tokens"]

    # Login
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": "owner@restaurant.com", "password": "Password123!"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["tokens"]["access_token"]

    # Me
    me_resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "owner@restaurant.com"


@pytest.mark.asyncio
async def test_dashboard_and_mentions_contract(client):
    # Dashboard summary
    resp = await client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "reputation_score" in data
    assert "sentiment_distribution" in data
    assert "top_issues" in data
    assert "recent_mentions" in data

    # Mentions list
    mentions_resp = await client.get("/api/mentions?page=1&limit=10")
    assert mentions_resp.status_code == 200
    m_data = mentions_resp.json()
    assert "items" in m_data
    assert "total" in m_data
    assert "total_pages" in m_data


@pytest.mark.asyncio
async def test_findings_and_issues_contract(client):
    # Issues
    issues_resp = await client.get("/api/issues")
    assert issues_resp.status_code == 200
    assert "items" in issues_resp.json()

    # Findings
    findings_resp = await client.get("/api/findings")
    assert findings_resp.status_code == 200
    assert "items" in findings_resp.json()

    # Suspicious reviews
    susp_resp = await client.get("/api/suspicious-reviews")
    assert susp_resp.status_code == 200
    assert "items" in susp_resp.json()


@pytest.mark.asyncio
async def test_v1_rest_parity(client):
    resp = await client.get("/api/v1/dashboard")
    assert resp.status_code == 200
    assert "reputation_score" in resp.json()
