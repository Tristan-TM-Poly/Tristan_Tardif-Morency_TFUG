from __future__ import annotations

from typing import Any


def compare_scores(prev: dict[str, Any], curr: dict[str, Any]) -> dict[str, float]:
    deltas = {}
    prev_scores = prev.get("dimension_scores", {})
    curr_scores = curr.get("dimension_scores", {})

    keys = set(prev_scores) | set(curr_scores)
    for k in keys:
        deltas[k] = float(curr_scores.get(k, 0.0)) - float(prev_scores.get(k, 0.0))
    return deltas


def summarize_evolution(history: list[dict[str, Any]]) -> dict[str, Any]:
    if len(history) < 2:
        return {"status": "insufficient_history"}
    prev = history[-2]
    curr = history[-1]
    return {
        "delta": compare_scores(prev, curr),
        "from_state": prev.get("profile_state"),
        "to_state": curr.get("profile_state"),
    }
