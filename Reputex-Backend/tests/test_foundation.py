"""Tests for Phase 1: Foundation, configuration, healthcheck, exceptions, and security."""

import pytest
from httpx import AsyncClient

from app.core.exceptions import UnauthorizedException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


@pytest.mark.asyncio
async def test_health_check_endpoints(client: AsyncClient):
    """Verify that both /health and /api/health return healthy status."""
    res1 = await client.get("/health")
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] == "healthy"
    assert data1["project"] == "RepuTex Backend"

    res2 = await client.get("/api/health")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "healthy"


def test_password_hashing_argon2():
    """Verify that Argon2id hashes passwords securely and verifies correctly."""
    plain = "MySecretPassw0rd!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_decoding():
    """Verify creation, decoding, and structure of JWT access and refresh tokens."""
    user_id = "usr_test_123"
    biz_id = "biz_test_456"
    access_token = create_access_token(subject=user_id, business_id=biz_id, role="owner")
    refresh_token = create_refresh_token(subject=user_id)

    # Decode access token
    payload = decode_token(access_token)
    assert payload["sub"] == user_id
    assert payload["business_id"] == biz_id
    assert payload["role"] == "owner"
    assert payload["type"] == "access"

    # Decode refresh token
    ref_payload = decode_token(refresh_token)
    assert ref_payload["sub"] == user_id
    assert ref_payload["type"] == "refresh"


def test_invalid_jwt_token():
    """Verify that tampered tokens raise UnauthorizedException."""
    with pytest.raises(UnauthorizedException) as exc_info:
        decode_token("invalid.token.string")
    assert exc_info.value.code == "INVALID_TOKEN"
