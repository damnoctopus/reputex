"""Business and Brand Keywords tests for Phase 2."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_business_and_keywords_lifecycle(client: AsyncClient):
    """Verify business setup wizard, keyword additions, and retrieval."""
    # Register user
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner@spicesymphony.com",
            "password": "Password123!",
            "full_name": "Spice Owner",
            "business_name": "Spice Symphony",
            "business_category": "Restaurant",
        },
    )
    token = reg_res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Fetch active business (/business)
    biz_res = await client.get("/api/business", headers=headers)
    assert biz_res.status_code == 200
    biz_data = biz_res.json()
    assert biz_data["name"] == "Spice Symphony"
    biz_id = biz_data["id"]

    # 2. Setup business wizard (/business)
    setup_payload = {
        "name": "Spice Symphony Indiranagar",
        "category": "Restaurant & Hospitality",
        "website": "https://spicesymphony.in",
        "location": "Indiranagar, Bengaluru",
        "phone": "+91 98765 43210",
        "keywords": ["Spice Symphony", "best biryani Indiranagar"],
        "platforms": ["Google", "JustDial", "Reddit", "X"],
    }
    setup_res = await client.post("/api/business", json=setup_payload, headers=headers)
    assert setup_res.status_code == 201
    setup_data = setup_res.json()
    assert setup_data["name"] == "Spice Symphony Indiranagar"
    assert setup_data["location"] == "Indiranagar, Bengaluru"
    assert len(setup_data["keywords"]) >= 2

    # 3. List Keywords (/keywords)
    kw_res = await client.get("/api/keywords", headers=headers)
    assert kw_res.status_code == 200
    kw_list = kw_res.json()
    assert len(kw_list) >= 2

    # 4. Add Brand Keyword (/keywords)
    add_kw_res = await client.post(
        "/api/keywords",
        json={"keyword": "butter garlic naan", "category": "brand"},
        headers=headers,
    )
    assert add_kw_res.status_code == 201
    new_kw = add_kw_res.json()
    assert new_kw["keyword"] == "butter garlic naan"
    new_kw_id = new_kw["id"]

    # 5. Delete Keyword (/keywords/{id})
    del_res = await client.delete(f"/api/keywords/{new_kw_id}", headers=headers)
    assert del_res.status_code == 204

    # 6. Update business (/businesses/{id})
    update_res = await client.put(
        f"/api/v1/businesses/{biz_id}",
        json={"description": "Premier fine-dining Indian restaurant in Bengaluru."},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["description"] == "Premier fine-dining Indian restaurant in Bengaluru."
