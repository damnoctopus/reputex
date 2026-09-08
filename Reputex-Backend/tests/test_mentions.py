"""Mentions and Reviews integration and filtering tests for Phase 3."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_mentions_pagination_and_filtering(client: AsyncClient):
    """Verify paginated mentions retrieval, facet filtering, and review detail."""
    # 1. Register User & Onboard Business
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "spice_mentions@spicesymphony.com",
            "password": "Password123!",
            "full_name": "Spice Manager",
            "business_name": "Spice Symphony",
            "business_category": "Restaurant",
        },
    )
    token = reg_res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Explicitly create test mentions via API
    for item in [
        {"platform": "Reddit", "author": "u/foodie", "content": "Great food", "sentiment": "positive", "rating": 5.0},
        {"platform": "Reddit", "author": "u/critic", "content": "Terrible service", "sentiment": "negative", "rating": 1.0},
        {"platform": "Google", "author": "Bot123", "content": "Bad spam review", "sentiment": "negative", "is_fake": True, "rating": 1.0},
        {"platform": "X", "author": "@diner", "content": "Amazing biryani!", "sentiment": "positive", "rating": 4.5},
        {"platform": "Google", "author": "Regular", "content": "Decent dinner", "sentiment": "neutral", "rating": 3.0},
    ]:
        await client.post("/api/mentions", json=item, headers=headers)

    feed_res = await client.get("/api/mentions", headers=headers)
    assert feed_res.status_code == 200
    feed_data = feed_res.json()
    assert "items" in feed_data
    assert "total_count" in feed_data
    assert feed_data["total_count"] >= 5
    items = feed_data["items"]
    first_item = items[0]
    assert "id" in first_item
    assert "platform" in first_item
    assert "content" in first_item
    assert "timestamp" in first_item  # Verified Flutter model requirement!

    mention_id = first_item["id"]

    # 3. Get mention by ID (/mentions/{id})
    detail_res = await client.get(f"/api/mentions/{mention_id}", headers=headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["id"] == mention_id

    # 4. Platform Filter (/mentions?platform=Reddit)
    reddit_res = await client.get("/api/mentions?platform=Reddit", headers=headers)
    assert reddit_res.status_code == 200
    reddit_items = reddit_res.json()["items"]
    assert all(m["platform"].lower() == "reddit" for m in reddit_items)

    # 5. Sentiment Filter (/mentions?sentiment=negative)
    neg_res = await client.get("/api/mentions?sentiment=negative", headers=headers)
    assert neg_res.status_code == 200
    neg_items = neg_res.json()["items"]
    assert all(m["sentiment"].lower() == "negative" for m in neg_items)

    # 6. Fake Review Filter (/mentions?is_fake=true)
    fake_res = await client.get("/api/mentions?is_fake=true", headers=headers)
    assert fake_res.status_code == 200
    fake_items = fake_res.json()["items"]
    assert all(m["is_fake"] is True for m in fake_items)

    # 7. Search query (/mentions?q=biryani)
    search_res = await client.get("/api/mentions?q=biryani", headers=headers)
    assert search_res.status_code == 200
    search_items = search_res.json()["items"]
    assert len(search_items) >= 1
    assert any("biryani" in m["content"].lower() for m in search_items)

    # 8. Reviews feed (/reviews)
    reviews_res = await client.get("/api/reviews", headers=headers)
    assert reviews_res.status_code == 200
    review_items = reviews_res.json()["items"]
    assert all(m["rating"] is not None for m in review_items)


@pytest.mark.asyncio
async def test_mentions_tenant_isolation(client: AsyncClient):
    """Verify that User A cannot view User B's mentions."""
    # Register User A
    res_a = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "userA_mentions@rest.com",
            "password": "Password123!",
            "full_name": "User A",
            "business_name": "Business A",
            "business_category": "Restaurant",
        },
    )
    token_a = res_a.json()["tokens"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B
    res_b = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "userB_mentions@rest.com",
            "password": "Password123!",
            "full_name": "User B",
            "business_name": "Business B",
            "business_category": "Retail",
        },
    )
    token_b = res_b.json()["tokens"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Create a mention for User A
    m_res = await client.post(
        "/api/mentions",
        json={"platform": "Reddit", "author": "u/test", "content": "Private review for A"},
        headers=headers_a,
    )
    mention_a_id = m_res.json()["id"]

    # User B attempts to access User A's mention -> 404 (Not Found in User B's tenant)
    unauthorized_fetch = await client.get(f"/api/mentions/{mention_a_id}", headers=headers_b)
    assert unauthorized_fetch.status_code == 404
    assert unauthorized_fetch.json()["error"]["code"] == "MENTION_NOT_FOUND"
