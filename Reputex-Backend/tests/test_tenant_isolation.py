"""Tenant Isolation & Multi-Tenant Authorization Security Tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_tenant_isolation_enforcement(client: AsyncClient):
    """Verify that User A cannot read, update, or delete Business B."""
    # Register User A with Business A
    res_a = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "userA@restaurantA.com",
            "password": "Password123!",
            "full_name": "User A",
            "business_name": "Business A",
            "business_category": "Restaurant",
        },
    )
    token_a = res_a.json()["tokens"]["access_token"]
    biz_a_id = res_a.json()["user"]["business_id"]

    # Register User B with Business B
    res_b = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "userB@restaurantB.com",
            "password": "Password123!",
            "full_name": "User B",
            "business_name": "Business B",
            "business_category": "Retail",
        },
    )
    token_b = res_b.json()["tokens"]["access_token"]
    biz_b_id = res_b.json()["user"]["business_id"]

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 1. User A accesses Business A -> Allowed (200)
    read_a_res = await client.get(f"/api/v1/businesses/{biz_a_id}", headers=headers_a)
    assert read_a_res.status_code == 200

    # 2. User A attempts to access Business B -> FORBIDDEN (403)
    hack_res = await client.get(f"/api/v1/businesses/{biz_b_id}", headers=headers_a)
    assert hack_res.status_code == 403
    assert hack_res.json()["error"]["code"] == "BUSINESS_ACCESS_DENIED"

    # 3. User A attempts to update Business B -> FORBIDDEN (403)
    hack_update = await client.put(
        f"/api/v1/businesses/{biz_b_id}",
        json={"name": "Hacked Business"},
        headers=headers_a,
    )
    assert hack_update.status_code == 403

    # 4. User A attempts to delete Business B -> FORBIDDEN (403)
    hack_delete = await client.delete(f"/api/v1/businesses/{biz_b_id}", headers=headers_a)
    assert hack_delete.status_code == 403

    # 5. User B still accesses Business B normally
    read_b_res = await client.get(f"/api/v1/businesses/{biz_b_id}", headers=headers_b)
    assert read_b_res.status_code == 200
    assert read_b_res.json()["name"] == "Business B"
