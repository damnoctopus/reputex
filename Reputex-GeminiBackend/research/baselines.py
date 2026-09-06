"""Baseline crisis models: Rule-based heuristics and logistic scorer."""
from typing import Dict


class HeuristicCrisisBaseline:
    """Deterministic rule-based baseline model."""
    def predict(self, features: Dict[str, float]) -> int:
        # Predict 1 (Crisis) if negative ratio > 0.4 and velocity > 5 or critical keywords present
        if features.get("critical_keyword_count", 0.0) >= 2.0 and features.get("negative_ratio", 0.0) > 0.3:
            return 1
        if features.get("negative_ratio", 0.0) >= 0.5 and features.get("complaint_velocity", 0.0) >= 4.0:
            return 1
        return 0

    def predict_proba(self, features: Dict[str, float]) -> float:
        score = (
            features.get("negative_ratio", 0.0) * 0.4 +
            min(1.0, features.get("complaint_velocity", 0.0) / 10.0) * 0.3 +
            min(1.0, features.get("critical_keyword_count", 0.0) / 3.0) * 0.3
        )
        return min(1.0, max(0.0, score))
