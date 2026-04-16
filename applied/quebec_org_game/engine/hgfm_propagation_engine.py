from __future__ import annotations

from collections import defaultdict
from typing import Any


def build_adjacency(edges: list[dict[str, Any]]) -> dict[str, list[tuple[str, float]]]:
    adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for edge in edges:
        source = str(edge.get("source"))
        target = str(edge.get("target"))
        weight = float(edge.get("weight", 1.0))
        adjacency[source].append((target, weight))
        adjacency[target].append((source, weight))
    return adjacency


def propagate_scores(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], damping: float = 0.25) -> list[dict[str, Any]]:
    score_map = {str(node.get("node_id")): float(node.get("score", 0.0)) for node in nodes}
    adjacency = build_adjacency(edges)
    updated = []

    for node in nodes:
        node_id = str(node.get("node_id"))
        propagated = score_map.get(node_id, 0.0)
        for neighbor, weight in adjacency.get(node_id, []):
            propagated += damping * weight * score_map.get(neighbor, 0.0)
        new_node = dict(node)
        new_node["propagated_score"] = propagated
        updated.append(new_node)
    return updated
