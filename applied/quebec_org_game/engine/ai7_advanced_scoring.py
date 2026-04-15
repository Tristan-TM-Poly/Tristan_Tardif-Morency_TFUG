from __future__ import annotations

from dataclasses import dataclass
from math import log1p
from typing import Iterable, Dict, Any


DEFAULT_DIMENSION_WEIGHTS = {
    "environment": 1.2,
    "labour": 1.1,
    "transparency": 1.0,
    "public_value": 1.0,
    "tax_fairness": 0.9,
    "competition": 0.9,
    "privacy": 0.9,
    "indigenous_relations": 1.2,
    "regional_development": 0.8,
    "safety": 1.1,
    "scientific_integrity": 1.0,
}


@dataclass
class AI7ScoreRow:
    dimension: str
    score: float
    confidence: float = 1.0
    source_reliability: float = 1.0
    recency_weight: float = 1.0
    network_weight: float = 1.0
    contradiction_penalty: float = 0.0


def nonlinear_weight(value: float) -> float:
    return max(0.1, log1p(max(value, 0.0)) + 0.5)


def advanced_weighted_value(row: AI7ScoreRow, dimension_weight: float) -> float:
    base = row.score * row.confidence * row.source_reliability * row.recency_weight
    network = nonlinear_weight(row.network_weight)
    contradiction = max(0.2, 1.0 - row.contradiction_penalty)
    return base * network * contradiction * dimension_weight


def compute_ai7_profile(rows: Iterable[AI7ScoreRow], dimension_weights: Dict[str, float] | None = None) -> Dict[str, Any]:
    dimension_weights = dimension_weights or DEFAULT_DIMENSION_WEIGHTS
    totals: Dict[str, float] = {k: 0.0 for k in dimension_weights}
    counts: Dict[str, int] = {k: 0 for k in dimension_weights}

    for row in rows:
        if row.dimension not in totals:
            totals[row.dimension] = 0.0
            counts[row.dimension] = 0
            dimension_weights[row.dimension] = 1.0
        totals[row.dimension] += advanced_weighted_value(row, dimension_weights[row.dimension])
        counts[row.dimension] += 1

    for dim, count in counts.items():
        if count > 0:
            totals[dim] /= count

    numerator = 0.0
    denominator = 0.0
    for dim, val in totals.items():
        weight = dimension_weights.get(dim, 1.0)
        numerator += val * weight
        denominator += weight

    total_score = numerator / denominator if denominator else 0.0

    if total_score >= 2.0:
        profile_state = "ai7_promote"
    elif total_score <= -2.0:
        profile_state = "ai7_quarantine"
    else:
        profile_state = "ai7_review"

    return {
        "dimension_scores": totals,
        "total_score": total_score,
        "profile_state": profile_state,
    }
