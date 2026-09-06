"""Explainability module for feature importance and crisis contribution breakdown."""
from typing import Dict, List, Tuple


def explain_prediction(features: Dict[str, float]) -> List[Tuple[str, float, str]]:
    """Explain which features contributed most to elevated risk."""
    weights = {
        "negative_ratio": 2.5,
        "sentiment_deterioration": -1.8,
        "complaint_velocity": 0.45,
        "engagement_growth": 0.35,
        "platform_spread": 0.40,
        "critical_keyword_count": 1.20,
    }

    explanations = []
    for k, w in weights.items():
        val = features.get(k, 0.0)
        contrib = val * w
        desc = f"Feature '{k}' value={val:.2f} contributed {contrib:+.2f} pts"
        explanations.append((k, round(contrib, 3), desc))

    # Sort by absolute contribution
    explanations.sort(key=lambda x: abs(x[1]), reverse=True)
    return explanations
