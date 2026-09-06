"""Feature engineering extracting statistical and text signals for crisis research."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
import math


def extract_features_from_mentions(
    mentions: List[Dict[str, Any]],
    as_of: datetime,
    window_hours: int = 48,
) -> Dict[str, float]:
    """Extract tabular research feature vector from historical mentions."""
    cutoff_recent = as_of - timedelta(hours=window_hours)
    cutoff_prior = as_of - timedelta(hours=window_hours * 2)

    recent = [m for m in mentions if cutoff_recent <= m["published_at"] <= as_of]
    prior = [m for m in mentions if cutoff_prior <= m["published_at"] < cutoff_recent]

    n_recent = len(recent)
    n_prior = len(prior)

    neg_recent = sum(1 for m in recent if m.get("sentiment") == "negative")
    neg_prior = sum(1 for m in prior if m.get("sentiment") == "negative")

    # Feature 1: Negative Ratio N_t
    negative_ratio = (neg_recent / n_recent) if n_recent > 0 else 0.0

    # Feature 2: Sentiment Deterioration Delta S
    s_recent = sum(m.get("sentiment_score", 0.0) for m in recent) / max(n_recent, 1)
    s_prior = sum(m.get("sentiment_score", 0.0) for m in prior) / max(n_prior, 1)
    delta_s = s_recent - s_prior

    # Feature 3: Complaint Velocity
    velocity = neg_recent / (window_hours / 24.0)

    # Feature 4: Engagement Growth G_t
    eng_recent = sum(
        m.get("engagement", {}).get("likes", 0) + m.get("engagement", {}).get("retweets", 0) + m.get("engagement", {}).get("upvotes", 0)
        for m in recent
    )
    eng_prior = sum(
        m.get("engagement", {}).get("likes", 0) + m.get("engagement", {}).get("retweets", 0) + m.get("engagement", {}).get("upvotes", 0)
        for m in prior
    )
    eng_growth = (eng_recent - eng_prior) / max(eng_prior, 1.0) if eng_prior > 0 else (1.0 if eng_recent > 0 else 0.0)

    # Feature 5: Cross-platform entropy / spread
    platforms = {m.get("platform") for m in recent if m.get("sentiment") == "negative"}
    platform_spread = float(len(platforms))

    # Feature 6: Severe keywords count (food safety, poisoning, scam, lawsuit)
    critical_keywords = ["poisoning", "sick", "hospital", "contamination", "scam", "lawsuit", "police"]
    critical_count = sum(
        1 for m in recent
        if any(kw in m.get("content", "").lower() for kw in critical_keywords)
    )

    return {
        "negative_ratio": float(round(negative_ratio, 4)),
        "sentiment_deterioration": float(round(delta_s, 4)),
        "complaint_velocity": float(round(velocity, 4)),
        "engagement_growth": float(round(eng_growth, 4)),
        "platform_spread": platform_spread,
        "critical_keyword_count": float(critical_count),
        "total_recent_volume": float(n_recent),
    }
