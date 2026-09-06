"""Authentication and Session tests for Phase 2."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_registration_and_login_flow(client: AsyncClient):
    """Verify registration, login, token refresh, and profile fetching."""
    # 1. Register User
    reg_payload = {
        "email": "adira@spicesymphony.com",
        "password": "strongPassword123!",
        "full_name": "Adithya",
        "business_name": "Spice Symphony",
        "business_category": "Restaurant",
        "phone": "+91 98765 43210",
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "user" in reg_data
    assert "tokens" in reg_data
    assert reg_data["user"]["email"] == "adira@spicesymphony.com"
    assert reg_data["user"]["full_name"] == "Adithya"
    assert reg_data["user"]["business_id"] is not None

    access_token = reg_data["tokens"]["access_token"]
    refresh_token = reg_data["tokens"]["refresh_token"]

    # 2. Duplicate Registration Rejection
    dup_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_res.status_code == 409
    assert dup_res.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"

    # 3. Successful Login
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "adira@spicesymphony.com", "password": "strongPassword123!"},
    )
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["user"]["id"] == reg_data["user"]["id"]

    # 4. Failed Login (Wrong Password)
    bad_login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "adira@spicesymphony.com", "password": "WrongPassword!"},
    )
    assert bad_login_res.status_code == 401
    assert bad_login_res.json()["error"]["code"] == "INVALID_CREDENTIALS"

    # 5. Get Current User Profile (/auth/me)
    me_res = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "adira@spicesymphony.com"

    # Also test Flutter alias /api/auth/me
    alias_me_res = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert alias_me_res.status_code == 200

    # 6. Unauthenticated /auth/me
    unauth_res = await client.get("/api/v1/auth/me")
    assert unauth_res.status_code == 401

    # 7. Token Refresh
    refresh_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_res.status_code == 200
    refreshed_tokens = refresh_res.json()
    assert "access_token" in refreshed_tokens
    assert "refresh_token" in refreshed_tokens
