import json
from applied.quebec_org_game.engine.hgfm_visualizer import export_graph


def build_graph_report(nodes, edges, config_path):
    graph_path = "out/tfuga/hgfm_graph.json"
    export_graph(nodes, edges, graph_path)

    summary = {
        "node_count": len(nodes),
        "edge_count": len(edges)
    }

    with open("out/tfuga/hgfm_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return graph_path
