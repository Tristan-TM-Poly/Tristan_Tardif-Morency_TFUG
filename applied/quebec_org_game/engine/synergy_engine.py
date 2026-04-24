def compute_synergy(node_a, node_b):
    shared_tags = set(node_a.get("tags", [])) & set(node_b.get("tags", []))
    return len(shared_tags)


def compute_graph_synergy(nodes):
    synergy_map = {}
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            key = (a["node_id"], b["node_id"])
            synergy_map[key] = compute_synergy(a, b)
    return synergy_map
