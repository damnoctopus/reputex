"""Deterministic offline mock Gemini provider matching all test cases and demo scenarios."""
from typing import Any, Dict, List, Optional
from app.schemas.gemini import (
    GeminiAspectItem,
    GeminiIssueItem,
    GeminiLinguisticSignals,
    GeminiMentionAnalysis,
)


class MockGeminiProvider:
    """100% deterministic offline intelligence provider with zero network dependencies."""

    def analyze_mentions_batch(
        self,
        mentions: List[Dict[str, Any]],
        business_name: str,
        business_category: str = "General",
    ) -> List[GeminiMentionAnalysis]:
        results: List[GeminiMentionAnalysis] = []
        for idx, m in enumerate(mentions):
            content = str(m.get("content", "")).lower()
            rating = m.get("rating")
            platform = str(m.get("platform", "")).lower()

            # Linguistic markers detection
            templated = 0.85 if any(p in content for p in ["best place in town", "highly recommended to all", "5 stars!", "simply the best"]) else 0.05
            superlatives = 0.90 if any(p in content for p in ["incredible", "phenomenal", "best ever", "spectacular"]) else 0.10
            operational = 0.15 if templated > 0.5 else 0.75

            # Sentiment determination
            if any(w in content for w in ["terrible", "horrible", "worst", "poisoning", "rude", "scam", "unacceptable", "dirty", "sick", "awful"]):
                sentiment_label = "negative"
                sentiment_score = -0.75
                confidence = 0.94
                intent = "complaint"
            elif any(w in content for w in ["amazing", "delicious", "great", "loved", "wonderful", "excellent", "favorite", "best"]):
                sentiment_label = "positive"
                sentiment_score = 0.80
                confidence = 0.92
                intent = "praise"
            else:
                sentiment_label = "neutral"
                sentiment_score = 0.0
                confidence = 0.80
                intent = "feedback"

            # Issue extraction
            issues: List[GeminiIssueItem] = []
            if any(w in content for w in ["rude", "ignored", "staff", "behavior", "unfriendly", "attitude"]):
                issues.append(GeminiIssueItem(
                    category="Customer Service",
                    subtopic="Staff Behavior",
                    severity="high",
                    excerpt=m.get("content", "")[:120],
                ))
            if any(w in content for w in ["slow", "wait", "waiting", "delay", "hour"]):
                issues.append(GeminiIssueItem(
                    category="Wait Times",
                    subtopic="Slow Service",
                    severity="medium",
                    excerpt=m.get("content", "")[:120],
                ))
            if any(w in content for w in ["charge", "bill", "fee", "hidden", "overcharged", "pricing"]):
                issues.append(GeminiIssueItem(
                    category="Billing",
                    subtopic="Hidden Fees",
                    severity="high",
                    excerpt=m.get("content", "")[:120],
                ))
            if any(w in content for w in ["cold", "raw", "taste", "food quality", "undercooked"]):
                issues.append(GeminiIssueItem(
                    category="Food Quality",
                    subtopic="Undercooked / Cold Food",
                    severity="high",
                    excerpt=m.get("content", "")[:120],
                ))
            if any(w in content for w in ["poisoning", "sick", "hospital", "vomit", "contamination"]):
                issues.append(GeminiIssueItem(
                    category="Food Safety",
                    subtopic="Food Poisoning Incident",
                    severity="critical",
                    excerpt=m.get("content", "")[:120],
                ))

            # Aspects extraction
            aspects: List[GeminiAspectItem] = []
            if "food" in content:
                aspects.append(GeminiAspectItem(aspect="Food", sentiment=sentiment_label, confidence=0.9))
            if any(w in content for w in ["service", "staff", "waiter", "server"]):
                aspects.append(GeminiAspectItem(aspect="Service", sentiment="negative" if "rude" in content or "slow" in content else sentiment_label, confidence=0.9))
            if any(w in content for w in ["price", "bill", "expensive", "worth"]):
                aspects.append(GeminiAspectItem(aspect="Pricing", sentiment="negative" if "charge" in content else "neutral", confidence=0.85))

            results.append(GeminiMentionAnalysis(
                mention_index=idx,
                sentiment_label=sentiment_label,
                confidence=confidence,
                sentiment_score=sentiment_score,
                intent=intent,
                issues=issues,
                aspects=aspects,
                linguistic_signals=GeminiLinguisticSignals(
                    templated_language=templated,
                    excessive_superlatives=superlatives,
                    operational_detail=operational,
                    unusual_patterns=0.75 if (rating == 5 and templated > 0.7) else 0.05,
                ),
                summary=f"Customer shared {sentiment_label} feedback on {m.get('platform')}.",
            ))

        return results

    def generate_response_draft(
        self,
        review_text: str,
        tone: str,
        business_name: str,
        custom_instructions: Optional[str] = None,
    ) -> str:
        if "rude" in review_text.lower() or "terrible" in review_text.lower() or "poisoning" in review_text.lower():
            return f"Dear Customer, thank you for bringing this to our attention. At {business_name}, we take our service and safety standards extremely seriously. Please contact our management team directly so we can make this right immediately."
        return f"Hello! Thank you so much for your kind words and for taking the time to review {business_name}. We look forward to serving you again soon!"
