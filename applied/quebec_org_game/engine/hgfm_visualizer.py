import json


def export_graph(nodes, edges, output_path="hgfm_graph.json"):
    graph = {
        "nodes": nodes,
        "edges": edges
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)


def build_simple_view(graph):
    print("HGFM GRAPH SUMMARY")
    print(f"Nodes: {len(graph.get('nodes', []))}")
    print(f"Edges: {len(graph.get('edges', []))}")
