"""Evaluation metrics for crisis detection: Precision, Recall, F1, and Mean Early Detection Latency (MEDL)."""
from typing import List, Tuple


def compute_classification_metrics(y_true: List[int], y_pred: List[int]) -> dict:
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)

    precision = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / max(len(y_true), 1)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def compute_medl(timelines: List[Tuple[float, float]]) -> float:
    """Compute Mean Early Detection Latency (hours detected before peak crisis)."""
    if not timelines:
        return 0.0
    latencies = [max(0.0, peak - detected) for detected, peak in timelines]
    return round(sum(latencies) / len(latencies), 2)
