from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


DEFAULT_WEIGHTS: Dict[str, float] = {
    "environment": 1.0,
    "labour": 1.0,
    "transparency": 0.9,
    "public_value": 1.0,
    "tax_fairness": 0.8,
    "competition": 0.8,
    "privacy": 0.8,
    "indigenous_relations": 1.0,
    "regional_development": 0.7,
    "safety": 1.0,
    "scientific_integrity": 0.9,
}


@dataclass
class EventDimensionScore:
    dimension: str
    score: float
    confidence: float = 1.0
    source_reliability: float = 1.0
    recency_weight: float = 1.0

    def weighted_value(self, dimension_weight: float) -> float:
        return self.score * self.confidence * self.source_reliability * self.recency_weight * dimension_weight


@dataclass
class OrganizationProfile:
    org_id: str
    dimension_scores: Dict[str, float]
    total_score: float
    profile_state: str


def aggregate_dimension_scores(
    rows: Iterable[EventDimensionScore],
    weights: Dict[str, float] | None = None,
) -> Dict[str, float]:
    weights = weights or DEFAULT_WEIGHTS
    totals: Dict[str, float] = {k: 0.0 for k in weights}
    counts: Dict[str, float] = {k: 0.0 for k in weights}

    for row in rows:
        if row.dimension not in totals:
            totals[row.dimension] = 0.0
            counts[row.dimension] = 0.0
            weights.setdefault(row.dimension, 1.0)
        value = row.weighted_value(weights[row.dimension])
        totals[row.dimension] += value
        counts[row.dimension] += 1.0

    for dim, count in counts.items():
        if count > 0:
            totals[dim] /= count

    return totals


def compute_total_score(dimension_scores: Dict[str, float], weights: Dict[str, float] | None = None) -> float:
    weights = weights or DEFAULT_WEIGHTS
    numerator = 0.0
    denominator = 0.0
    for dim, score in dimension_scores.items():
        w = weights.get(dim, 1.0)
        numerator += score * w
        denominator += w
    return numerator / denominator if denominator else 0.0


def infer_profile_state(total_score: float) -> str:
    if total_score >= 2.5:
        return "strong_positive"
    if total_score >= 0.75:
        return "positive"
    if total_score <= -2.5:
        return "strong_negative"
    if total_score <= -0.75:
        return "negative"
    return "mixed"


def build_organization_profile(org_id: str, rows: List[EventDimensionScore]) -> OrganizationProfile:
    dimension_scores = aggregate_dimension_scores(rows)
    total_score = compute_total_score(dimension_scores)
    profile_state = infer_profile_state(total_score)
    return OrganizationProfile(
        org_id=org_id,
        dimension_scores=dimension_scores,
        total_score=total_score,
        profile_state=profile_state,
    )
