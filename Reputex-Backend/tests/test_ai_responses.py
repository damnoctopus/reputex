"""Tests for Phase 6: AI Response Studio endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_response_studio_lifecycle(client: AsyncClient):
    # 1. Register User with Business
    reg_payload = {
        "email": "ai_editor@spicesymphony.com",
        "password": "SecurePassword123!",
        "full_name": "Rohan AI Editor",
        "business_name": "Spice AI Studio",
        "business_category": "Restaurant",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    token = res.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Fetch Mentions to get a mention ID
    m_res = await client.get("/api/v1/mentions", headers=headers)
    assert m_res.status_code == 200
    items = m_res.json()["items"]
    assert len(items) > 0
    mention_id = items[0]["id"]

    # 3. Generate Response Draft
    gen_payload = {
        "mention_id": mention_id,
        "tone": "empathetic",
        "custom_instructions": "Offer a 20% discount coupon on their next dinner reservation.",
    }
    gen_res = await client.post("/api/v1/responses/generate", json=gen_payload, headers=headers)
    assert gen_res.status_code == 201
    draft = gen_res.json()
    assert draft["mention_id"] == mention_id
    assert draft["tone"] == "empathetic"
    assert draft["status"] == "drafted"
    assert "20% discount" in draft["generated_response"]
    draft_id = draft["id"]

    # 4. List Responses
    list_res = await client.get("/api/v1/responses", headers=headers)
    assert list_res.status_code == 200
    drafts = list_res.json()
    assert isinstance(drafts, list)
    assert any(d["id"] == draft_id for d in drafts)

    # 5. Get Single Response
    single_res = await client.get(f"/api/v1/responses/{draft_id}", headers=headers)
    assert single_res.status_code == 200
    assert single_res.json()["id"] == draft_id

    # 6. Update Response Draft
    update_res = await client.put(
        f"/api/v1/responses/{draft_id}",
        json={"response_text": "Updated refined text by manager."},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["generated_response"] == "Updated refined text by manager."

    # 7. Approve Response Draft
    approve_res = await client.post(
        f"/api/v1/responses/{draft_id}/approve",
        json={"response_text": "Final approved executive response."},
        headers=headers,
    )
    assert approve_res.status_code == 200
    approved_draft = approve_res.json()
    assert approved_draft["status"] == "approved"
    assert approved_draft["approved_at"] is not None

    # 8. Dispatch Response
    dispatch_res = await client.post(f"/api/v1/responses/{draft_id}/dispatch", headers=headers)
    assert dispatch_res.status_code == 200
    dispatched_draft = dispatch_res.json()
    assert dispatched_draft["status"] == "dispatched"
    assert dispatched_draft["dispatched_at"] is not None

    # 9. Verify /ai/responses alias works as well
    ai_alias_res = await client.get(f"/api/v1/ai/responses/{draft_id}", headers=headers)
    assert ai_alias_res.status_code == 200
    assert ai_alias_res.json()["id"] == draft_id
