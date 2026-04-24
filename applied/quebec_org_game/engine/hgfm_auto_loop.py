from applied.quebec_org_game.engine.real_dataset_to_profiles import dataset_to_profiles
from applied.quebec_org_game.engine.hgfm_bridge import organizations_to_hgfm_nodes, events_to_hgfm_nodes, build_org_event_edges
from applied.quebec_org_game.engine.graph_report_pipeline import build_graph_report


def run_full_auto_loop(data_dir, config_path):
    profiles = dataset_to_profiles(data_dir, config_path)

    nodes = []
    edges = []

    for org_id, profile in profiles.items():
        nodes.append({
            "node_id": f"org::{org_id}",
            "label": org_id,
            "node_type": "organization"
        })

        nodes.append({
            "node_id": f"profile::{org_id}",
            "label": f"Profile {org_id}",
            "node_type": "profile",
            "score": profile["total_score"]
        })

        edges.append({
            "source": f"org::{org_id}",
            "target": f"profile::{org_id}",
            "relation": "has_profile"
        })

    graph_path = build_graph_report(nodes, edges, config_path)

    return graph_path
