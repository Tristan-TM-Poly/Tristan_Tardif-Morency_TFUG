from __future__ import annotations

from typing import Dict, Any, List


def profiles_to_hgfm_nodes(profiles: Dict[str, Any]) -> List[Dict[str, Any]]:
    nodes = []
    for org_id, profile in profiles.items():
        nodes.append({
            "node_id": f"profile::{org_id}",
            "label": f"Profile {org_id}",
            "node_type": "profile",
            "tags": [getattr(profile, 'profile_state', 'unknown')],
            "metadata": {
                "org_id": org_id,
                "total_score": getattr(profile, 'total_score', None),
                "dimension_scores": getattr(profile, 'dimension_scores', {}),
            },
        })
    return nodes


def build_org_profile_edges(profiles: Dict[str, Any]) -> List[Dict[str, Any]]:
    edges = []
    for org_id in profiles:
        edges.append({
            "source": f"org::{org_id}",
            "target": f"profile::{org_id}",
            "relation": "has_profile",
            "weight": 1.0,
        })
    return edges
