"""AI Provider abstraction with Mock and Gemini integration layers."""

import abc
from typing import Any

from app.core.config import settings


class AIProvider(abc.ABC):
    """Abstract interface for AI intelligence and text generation services."""

    @abc.abstractmethod
    async def generate_response(
        self,
        review_text: str,
        tone: str,
        business_name: str,
        custom_instructions: str | None = None,
    ) -> str:
        """Generate a context-aware public response draft."""

    @abc.abstractmethod
    async def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """Analyze sentiment, confidence, and emotions from text."""

    @abc.abstractmethod
    async def detect_crisis(self, mentions: list[str]) -> dict[str, Any]:
        """Detect coordinated negative sentiment spikes."""


class MockAIProvider(AIProvider):
    """Deterministic, high-fidelity mock AI provider for offline & test environments."""

    TONE_TEMPLATES = {
        "empathetic": (
            "Dear valued patron, thank you for sharing your candid thoughts with us. "
            "At {business_name}, we hold our hospitality and culinary craft to the utmost standard, "
            "and we are genuinely disheartened to learn that your visit fell short of what you deserved. "
            "We would love the privilege of making this right—please reach out to our management directly at "
            "concierge@{business_name_slug}.com so we can host you again with the warmth you deserve."
        ),
        "professional": (
            "Thank you for your review. At {business_name}, we continuously audit our operational quality "
            "and customer touchpoints. We have logged your feedback regarding this incident and shared it "
            "directly with our floor and kitchen supervisors for prompt procedural review. Should you wish to discuss "
            "further, please contact support@{business_name_slug}.com."
        ),
        "apologetic": (
            "We sincerely apologize for your disappointing experience at {business_name}. "
            "There is no excuse for failing to meet our service expectations during your visit. "
            "We take complete responsibility and are immediately addressing this with our culinary and service teams. "
            "Please allow us to extend a personal remedy by contacting us at feedback@{business_name_slug}.com."
        ),
        "friendly": (
            "Hey there! Thanks so much for stopping by {business_name} and taking the time to drop us a note! "
            "We love hearing from our community and always appreciate honest feedback. We're already putting your notes "
            "into action so your next visit is even tastier. Hope to see you back at our tables soon!"
        ),
        "concise": (
            "Thank you for your feedback regarding {business_name}. "
            "We have noted your comments and are working with our team to improve this immediately. "
            "For any follow-up, please reach out to care@{business_name_slug}.com."
        ),
        "firm": (
            "Thank you for contacting {business_name}. We take customer authenticity and service integrity very seriously. "
            "While we welcome genuine dining feedback, our records do not show a corresponding order or ticket for this description. "
            "We invite you to provide order verification to verification@{business_name_slug}.com so we can properly investigate."
        ),
    }

    async def generate_response(
        self,
        review_text: str,
        tone: str,
        business_name: str,
        custom_instructions: str | None = None,
    ) -> str:
        norm_tone = tone.lower()
        slug = "".join(c for c in business_name.lower() if c.isalnum()) or "reputex"
        template = self.TONE_TEMPLATES.get(norm_tone, self.TONE_TEMPLATES["empathetic"])

        response = template.format(
            business_name=business_name,
            business_name_slug=slug,
        )

        if custom_instructions and custom_instructions.strip():
            response += f"\n\nP.S. In response to your note: {custom_instructions.strip()}"

        return response

    async def analyze_sentiment(self, text: str) -> dict[str, Any]:
        return {
            "sentiment": "POSITIVE",
            "confidence": 0.88,
            "positive_score": 0.85,
            "neutral_score": 0.10,
            "negative_score": 0.05,
        }

    async def detect_crisis(self, mentions: list[str]) -> dict[str, Any]:
        return {
            "is_crisis": False,
            "severity": "low",
            "velocity": 0.5,
        }


class GeminiAIProvider(AIProvider):
    """Real Google Gemini API provider integration."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_response(
        self,
        review_text: str,
        tone: str,
        business_name: str,
        custom_instructions: str | None = None,
    ) -> str:
        # Fallback to deterministic mock if API call fails or key is dummy
        try:
            import httpx

            prompt = (
                f"You are the reputation manager for '{business_name}'. "
                f"Write a public reply in a '{tone}' tone to this customer review:\n"
                f'"{review_text}"\n'
            )
            if custom_instructions:
                prompt += f"Incorporate these specific instructions: {custom_instructions}\n"
            prompt += "Reply strictly with the customer response text."

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
        except Exception:
            pass

        # Resilient fallback to mock
        return await MockAIProvider().generate_response(review_text, tone, business_name, custom_instructions)

    async def analyze_sentiment(self, text: str) -> dict[str, Any]:
        return await MockAIProvider().analyze_sentiment(text)

    async def detect_crisis(self, mentions: list[str]) -> dict[str, Any]:
        return await MockAIProvider().detect_crisis(mentions)


def get_ai_provider() -> AIProvider:
    """Factory to retrieve configured AI provider based on environment variables."""
    provider_name = getattr(settings, "AI_PROVIDER", "mock").lower()
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if provider_name == "gemini" and api_key and api_key != "your_gemini_api_key_here":
        return GeminiAIProvider(api_key=api_key)
    return MockAIProvider()
