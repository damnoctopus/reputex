"""Tests for Gemini Client, batching, structured schemas, and mock fallback."""
import pytest
from app.ai.gemini_client import GeminiClient
from app.ai.mock_gemini import MockGeminiProvider
from app.schemas.gemini import GeminiBatchMentionAnalysis, GeminiMentionAnalysis


def test_mock_gemini_batch_analysis():
    provider = MockGeminiProvider()
    mentions = [
        {"content": "Amazing delicious dinner! Best place in town.", "rating": 5.0, "platform": "google"},
        {"content": "Rude staff and slow service! Waited 45 minutes for drinks.", "rating": 1.0, "platform": "google"},
        {"content": "Severe food poisoning after eating here. Sick all night!", "rating": 1.0, "platform": "twitter"},
    ]

    analyses = provider.analyze_mentions_batch(mentions, business_name="Spice Symphony")
    assert len(analyses) == 3

    # Mention 0: Positive
    assert analyses[0].sentiment_label == "positive"
    assert analyses[0].sentiment_score > 0.5
    assert analyses[0].intent == "praise"

    # Mention 1: Negative - Customer service
    assert analyses[1].sentiment_label == "negative"
    assert any(iss.category == "Customer Service" for iss in analyses[1].issues)

    # Mention 2: Food safety
    assert analyses[2].sentiment_label == "negative"
    assert any(iss.category == "Food Safety" for iss in analyses[2].issues)


def test_gemini_client_fallback_when_offline():
    # Without api_key, should fallback cleanly to MockGeminiProvider
    client = GeminiClient(api_key="")
    assert not client.is_available

    mentions = [{"content": "Great food and polite waiters.", "platform": "google"}]
    analyses = client.analyze_mentions_batch(mentions, "Spice Symphony")
    assert len(analyses) == 1
    assert analyses[0].sentiment_label == "positive"


def test_response_draft_generation():
    provider = MockGeminiProvider()
    draft = provider.generate_response_draft(
        review_text="Rude staff ignored us for an hour!",
        tone="professional",
        business_name="Spice Symphony",
    )
    assert "Spice Symphony" in draft
    assert "attention" in draft.lower() or "service" in draft.lower()
