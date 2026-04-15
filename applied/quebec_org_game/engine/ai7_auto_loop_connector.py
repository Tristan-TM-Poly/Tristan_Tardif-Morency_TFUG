from __future__ import annotations

from applied.quebec_org_game.engine.real_dataset_to_profiles import dataset_to_profiles
from applied.quebec_org_game.engine.ai7_advanced_scoring import AI7ScoreRow, compute_ai7_profile
from applied.quebec_org_game.engine.ai7_hgfm_feedback import inject_ai7_feedback
from applied.quebec_org_game.engine.graph_report_pipeline import build_graph_report


def profile_to_ai7_rows(profile_key: str, profile_payload: dict) -> list[AI7ScoreRow]:
    base_score = float(profile_payload.get("total_score", 0.0))
    event_count = len(profile_payload.get("events", []))
    network_weight = max(1.0, event_count)
    return [
        AI7ScoreRow(
            dimension="public_value",
            score=base_score,
            confidence=0.7,
            source_reliability=0.7,
            recency_weight=1.0,
            network_weight=network_weight,
            contradiction_penalty=0.0,
        )
    ]


def run_ai7_auto_loop(data_dir: str, config_path: str):
    raw_profiles = dataset_to_profiles(data_dir, config_path)
    ai7_profiles = {}

    for profile_key, payload in raw_profiles.items():
        rows = profile_to_ai7_rows(profile_key, payload)
        ai7_profiles[profile_key] = compute_ai7_profile(rows)

    nodes = []
    edges = []
    for profile_key, payload in ai7_profiles.items():
        nodes.append({
            "node_id": f"org::{profile_key}",
            "label": profile_key,
            "node_type": "organization",
        })
        nodes.append({
            "node_id": f"profile::{profile_key}",
            "label": f"Profile {profile_key}",
            "node_type": "profile",
        })
        edges.append({
            "source": f"org::{profile_key}",
            "target": f"profile::{profile_key}",
            "relation": "has_profile",
        })

    nodes = inject_ai7_feedback(nodes, ai7_profiles)
    graph_path = build_graph_report(nodes, edges, "applied/quebec_org_game/config/hgfm_visual_config.json")

    return {
        "profiles": ai7_profiles,
        "graph_path": graph_path,
    }
