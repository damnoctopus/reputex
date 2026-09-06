"""Tests for the isolated research crisis modeling and feature engineering module."""
from datetime import datetime, timezone
import pytest
from research.baselines import HeuristicCrisisBaseline
from research.crisis_model import ResearchCrisisModel
from research.evaluation import compute_classification_metrics, compute_medl
from research.explainability import explain_prediction
from research.feature_engineering import extract_features_from_mentions


def test_research_feature_engineering_and_models():
    now = datetime.now(timezone.utc)
    mock_mentions = [
        {"published_at": now, "sentiment": "negative", "sentiment_score": -0.8, "content": "Food poisoning hospital emergency!", "engagement": {"likes": 50, "retweets": 20}},
        {"published_at": now, "sentiment": "negative", "sentiment_score": -0.7, "content": "Rude staff and slow service", "engagement": {"likes": 10}},
        {"published_at": now, "sentiment": "positive", "sentiment_score": 0.8, "content": "Good ambiance", "engagement": {"likes": 5}},
    ]

    features = extract_features_from_mentions(mock_mentions, as_of=now, window_hours=48)
    assert "negative_ratio" in features
    assert "sentiment_deterioration" in features
    assert features["critical_keyword_count"] >= 1.0

    # Baseline prediction
    baseline = HeuristicCrisisBaseline()
    pred_base = baseline.predict(features)
    assert pred_base in [0, 1]

    # ML model prediction
    model = ResearchCrisisModel()
    pred_ml = model.predict(features)
    prob_ml = model.predict_proba(features)
    assert 0.0 <= prob_ml <= 1.0

    # Explainability
    explanations = explain_prediction(features)
    assert len(explanations) > 0
    assert any("negative_ratio" in exp[0] for exp in explanations)

    # Metrics
    metrics = compute_classification_metrics([1, 0, 1, 1], [1, 0, 0, 1])
    assert metrics["precision"] > 0.5
    assert metrics["recall"] > 0.5

    medl = compute_medl([(10.0, 16.0), (12.0, 18.0)])
    assert medl == 6.0
