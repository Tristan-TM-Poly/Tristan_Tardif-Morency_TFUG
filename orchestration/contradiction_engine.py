from __future__ import annotations

from typing import Any


def detect_contradictions(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contradictions = []
    by_subject: dict[str, list[dict[str, Any]]] = {}

    for claim in claims:
        subject = str(claim.get("subject", "unknown"))
        by_subject.setdefault(subject, []).append(claim)

    for subject, rows in by_subject.items():
        polarities = {str(r.get("polarity", "unknown")) for r in rows}
        if "positive" in polarities and "negative" in polarities:
            contradictions.append({
                "subject": subject,
                "status": "contradiction_detected",
                "claim_count": len(rows),
            })
    return contradictions


def contradiction_penalty(contradictions: list[dict[str, Any]]) -> float:
    if not contradictions:
        return 0.0
    return min(0.8, 0.2 * len(contradictions))
