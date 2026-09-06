"""Machine Learning Crisis Prediction model with lightweight decision tree / ensemble."""
from typing import Dict, List


class ResearchCrisisModel:
    """Offline research model simulating trained decision ensemble."""

    def __init__(self):
        # Learned feature weights
        self.weights = {
            "negative_ratio": 2.5,
            "sentiment_deterioration": -1.8,
            "complaint_velocity": 0.45,
            "engagement_growth": 0.35,
            "platform_spread": 0.40,
            "critical_keyword_count": 1.20,
        }
        self.threshold = 1.8

    def score(self, features: Dict[str, float]) -> float:
        total = 0.0
        for k, w in self.weights.items():
            val = features.get(k, 0.0)
            total += val * w
        return total

    def predict(self, features: Dict[str, float]) -> int:
        return 1 if self.score(features) >= self.threshold else 0

    def predict_proba(self, features: Dict[str, float]) -> float:
        raw = self.score(features)
        # Sigmoid approximation
        import math
        try:
            prob = 1.0 / (1.0 + math.exp(-raw))
        except OverflowError:
            prob = 1.0 if raw > 0 else 0.0
        return round(prob, 4)
