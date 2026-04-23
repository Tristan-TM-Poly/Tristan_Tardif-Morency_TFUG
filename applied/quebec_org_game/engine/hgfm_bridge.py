from __future__ import annotations

from typing import Dict, List, Any


def organizations_to_hgfm_nodes(organizations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    nodes = []
    for org in organizations:
        nodes.append({
            "node_id": f"org::{org['org_id']}",
            "label": org["name"],
            "node_type": "organization",
            "tags": [org.get("org_type", "unknown"), org.get("sector", "unknown")],
            "metadata": org,
        })
    return nodes


def events_to_hgfm_nodes(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    nodes = []
    for event in events:
        nodes.append({
            "node_id": f"event::{event['event_id']}",
            "label": event["event_title"],
            "node_type": "event",
            "tags": [event.get("event_type", "unknown"), event.get("impact_direction", "unknown")],
            "metadata": event,
        })
    return nodes


def build_org_event_edges(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    edges = []
    for event in events:
        edges.append({
            "source": f"org::{event['org_id']}",
            "target": f"event::{event['event_id']}",
            "relation": "has_event",
            "weight": 1.0,
        })
    return edges
