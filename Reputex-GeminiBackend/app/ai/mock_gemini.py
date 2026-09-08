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

    async def assess_reputation_deterioration(
        self,
        business_name: str,
        business_category: str,
        review_summary: str,
        recent_reviews: list[dict],
        horizon_days: int = 14,
    ) -> GeminiDeteriorationResponse:
        """Deterministic mock evaluation of future reputation deterioration."""
        from app.schemas.gemini import GeminiDeteriorationResponse

        total = len(recent_reviews)
        negative_count = sum(
            1 for r in recent_reviews
            if (r.get("rating") is not None and r.get("rating") <= 2.0)
            or any(w in r.get("content", "").lower() for w in ["horrible", "rude", "worst", "attitude", "bad", "terrible", "awful", "unacceptable", "cold", "dirty"])
        )
        neg_ratio = negative_count / max(total, 1)

        if neg_ratio >= 0.25 or negative_count >= 5:
            probability = min(0.60 + (neg_ratio * 0.35), 0.95)
            risk_level = "HIGH" if probability < 0.80 else "CRITICAL"
            is_sustained = True
            drivers = [
                f"Negative feedback constitutes {neg_ratio*100:.1f}% of recent customer mentions",
                "Complaints are recurring across multiple platforms (Google, Reddit, X)",
                "Specific convergence on service quality, wait times, and staff behavior",
            ]
            converging = ["Customer Service & Staff Behavior", "Wait Time & Delays", "Food Quality Consistency"]
            opinion = (
                f"Based on recent customer mentions across platforms, {business_name} is showing clear indicators "
                f"of a sustained reputation decline rather than an isolated blip. Negative mentions are converging on "
                f"specific operational pain points with high emotional intensity. Without proactive management intervention, "
                f"overall customer trust and rating trajectories are projected to deteriorate further over the next {horizon_days} days."
            )
            actions = [
                "Address staff behavior and front-of-house training immediately.",
                "Publicly respond to top negative Reddit and Google reviews with empathetic resolution offers.",
                "Monitor social mentions daily to intercept viral complaints before escalation.",
            ]
        else:
            probability = max(0.12, neg_ratio * 0.6)
            risk_level = "LOW" if probability < 0.35 else "MODERATE"
            is_sustained = False
            drivers = [
                "Customer sentiment is predominantly positive or neutral",
                "Isolated negative complaints lack topical convergence",
                "Rating distribution remains stable relative to historical baseline",
            ]
            converging = []
            opinion = (
                f"Recent negative feedback for {business_name} represents normal, isolated customer variance (a temporary blip) "
                f"rather than a systematic decline. Core customer satisfaction signals remain healthy across Google, Reddit, and X."
            )
            actions = [
                "Continue standard quality assurance and customer care.",
                "Acknowledge constructive customer feedback politely.",
            ]

        return GeminiDeteriorationResponse(
            deterioration_probability=round(probability, 2),
            risk_level=risk_level,
            is_sustained_decline=is_sustained,
            confidence=0.88,
            key_drivers=drivers,
            converging_complaints=converging,
            expert_opinion=opinion,
            recommended_actions=actions,
        )


MockGeminiClient = MockGeminiProvider
