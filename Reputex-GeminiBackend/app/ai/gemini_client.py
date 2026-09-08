import asyncio
"""Centralized Google Gemini Client with Google Search Grounding & structured batching."""
import json
import logging
import time
from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from app.core.config import settings
from app.schemas.gemini import (
    GeminiAspectItem,
    GeminiBatchMentionAnalysis,
    GeminiIssueItem,
    GeminiLinguisticSignals,
    GeminiMentionAnalysis,
)

logger = logging.getLogger("reputex.gemini")


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Google GenAI client: {e}")

    @property
    def is_available(self) -> bool:
        return self._client is not None and bool(self.api_key)

    def search_with_grounding(
        self,
        query: str,
        business_name: str,
        location: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Execute a grounded Google search to discover recent public mentions across Google, Reddit, and X."""
        if not self.is_available:
            logger.info("Gemini client not available for search grounding, returning empty citations")
            return []

        from google.genai import types

        prompt = f"""Find recent public web discussions, customer reviews, complaints, and mentions about the business '{business_name}' located in '{location or 'any'}'.
Focus on queries: {query}
Extract key quotes, platform source (Google, Reddit, X/Twitter, or Web), author name where mentioned, approximate date or freshness, and exact source URLs."""

        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.1,
        )

        retries = settings.GEMINI_MAX_RETRIES
        delay = 2.0
        for attempt in range(retries):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )

                citations = []
                # Extract grounding metadata citations if present
                candidate = response.candidates[0] if response.candidates else None
                if candidate and hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    gm = candidate.grounding_metadata
                    if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                        for idx, chunk in enumerate(gm.grounding_chunks):
                            web = getattr(chunk, 'web', None)
                            if web:
                                citations.append({
                                    "title": getattr(web, 'title', ''),
                                    "url": getattr(web, 'uri', ''),
                                    "snippet": response.text[:400] if response.text else "",
                                    "index": idx,
                                })

                # If no chunks explicitly extracted, use the grounded text
                if not citations and response.text:
                    citations.append({
                        "title": f"{business_name} Search Result",
                        "url": f"https://www.google.com/search?q={query}",
                        "snippet": response.text[:600],
                        "index": 0,
                    })

                return citations
            except Exception as e:
                logger.warning(f"Gemini search grounding attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    logger.error(f"Gemini search grounding failed after {retries} attempts: {e}")
                    return []

        return []

    def analyze_mentions_batch(
        self,
        mentions: List[Dict[str, Any]],
        business_name: str,
        business_category: str = "General",
    ) -> List[GeminiMentionAnalysis]:
        """Run batched structured semantic analysis on a list of mentions."""
        if not mentions:
            return []

        if not self.is_available:
            from app.ai.mock_gemini import MockGeminiProvider
            mock_provider = MockGeminiProvider()
            return mock_provider.analyze_mentions_batch(mentions, business_name, business_category)

        from google.genai import types

        formatted_items = []
        for idx, m in enumerate(mentions):
            formatted_items.append(
                f"Mention #{idx} (Platform: {m.get('platform')}, Rating: {m.get('rating')}, Author: {m.get('author')}):\n\"{m.get('content', '')}\""
            )
        batch_text = "\n\n".join(formatted_items)

        prompt = f"""You are the senior reputation intelligence engine for business '{business_name}' (Category: {business_category}).
Analyze the following batch of {len(mentions)} customer mentions and reviews.
For each mention:
1. Determine sentiment ('positive', 'neutral', 'negative'), confidence (0.0-1.0), and sentiment_score (-1.0 to 1.0).
2. Classify intent ('complaint', 'praise', 'inquiry', 'recommendation', 'neutral_feedback').
3. Extract specific customer issues/problems with category (e.g., Customer Service, Billing, Food Quality, Delays), subtopic, severity ('low', 'medium', 'high', 'critical'), and supporting verbatim excerpt.
4. Extract aspects (e.g. Service, Food, Pricing, Staff) and sentiment.
5. Score linguistic suspicion indicators (templated_language, excessive_superlatives, operational_detail, unusual_patterns) from 0.0 to 1.0.
6. Provide a 1-sentence summary.

Return structured JSON conforming to GeminiBatchMentionAnalysis with an item for each mention indexed from 0 to {len(mentions)-1}.

Mentions to analyze:
{batch_text}"""

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiBatchMentionAnalysis,
            temperature=0.1,
        )

        retries = settings.GEMINI_MAX_RETRIES
        delay = 2.0
        for attempt in range(retries):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )

                if response.text:
                    parsed = GeminiBatchMentionAnalysis.model_validate_json(response.text)
                    if parsed.analyses:
                        return parsed.analyses
            except Exception as e:
                logger.warning(f"Gemini batch analysis attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    logger.error(f"Gemini batch analysis failed after {retries} retries: {e}")

        # Fallback to deterministic mock parsing on API failure to prevent pipeline failure
        from app.ai.mock_gemini import MockGeminiProvider
        return MockGeminiProvider().analyze_mentions_batch(mentions, business_name, business_category)

    def generate_response_draft(
        self,
        review_text: str,
        tone: str,
        business_name: str,
        custom_instructions: Optional[str] = None,
    ) -> str:
        """Generate an AI customer response draft."""
        if not self.is_available:
            from app.ai.mock_gemini import MockGeminiProvider
            return MockGeminiProvider().generate_response_draft(review_text, tone, business_name, custom_instructions)

        prompt = f"""Draft a {tone} customer response on behalf of '{business_name}' to the following review:
\"{review_text}\"
{f'Additional instructions: {custom_instructions}' if custom_instructions else ''}
Provide only the finalized response text without preamble."""

        try:
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text.strip() if response.text else "Thank you for taking the time to share your feedback with us."
        except Exception as e:
            logger.error(f"Failed to generate response draft: {e}")
            return f"Thank you for reaching out to {business_name}. We take your feedback seriously and are actively working to address this issue."

    async def assess_reputation_deterioration(
        self,
        business_name: str,
        business_category: str,
        review_summary: str,
        recent_reviews: list[dict],
        horizon_days: int = 14,
    ) -> GeminiDeteriorationResponse:
        """Ask Gemini for its expert assessment on near-term reputation deterioration risk.

        Evaluates chronological customer reviews across Google, Reddit, and X to assess whether
        negative feedback is an isolated, temporary blip or the start of a sustained decline.
        """
        from app.schemas.gemini import GeminiDeteriorationResponse

        if settings.USE_MOCK_GEMINI or not self._client:
            from app.ai.mock_gemini import MockGeminiClient
            mock = MockGeminiClient()
            return await mock.assess_reputation_deterioration(
                business_name, business_category, review_summary, recent_reviews, horizon_days
            )

        reviews_text = "\n".join(
            f"[{r.get('platform', 'unknown').upper()}] {r.get('author', 'Anonymous')}: {r.get('content', '')} (Rating: {r.get('rating', 'N/A')})"
            for r in recent_reviews[:30]
        )

        prompt = f"""You are an elite corporate reputation intelligence analyst.
Analyze the following customer review history and recent public mentions across Google, Reddit, and X for the business "{business_name}" (Category: {business_category}).

Summary of recent review dynamics:
{review_summary}

Recent public mentions / customer reviews:
{reviews_text}

Task:
In your professional opinion:
1. What is the probability (from 0.00 to 1.00) that this business will experience near-term reputation deterioration in the next {horizon_days} days?
2. Is this recent negative feedback merely an isolated, temporary blip (noise), or does it signal the beginning of a sustained reputation decline?
3. What are the key warning signs and drivers (e.g., service breakdown, recurring quality defects, staff issues, or coordinated backlash)?
4. What specific issues or complaints are customers converging around?
5. Provide your detailed expert opinion explaining your analytical reasoning.
6. What practical mitigation steps should the owner take immediately?

Respond in strictly valid JSON conforming to the requested schema.
"""
        try:
            from google.genai import types
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GeminiDeteriorationResponse,
                    temperature=0.2,
                ),
            )
            return GeminiDeteriorationResponse.model_validate_json(response.text)
        except Exception as e:
            logger.warning("Gemini deterioration assessment failed: %s. Falling back to mock.", e)
            from app.ai.mock_gemini import MockGeminiClient
            return await MockGeminiClient().assess_reputation_deterioration(
                business_name, business_category, review_summary, recent_reviews, horizon_days
            )


gemini_client = GeminiClient()
