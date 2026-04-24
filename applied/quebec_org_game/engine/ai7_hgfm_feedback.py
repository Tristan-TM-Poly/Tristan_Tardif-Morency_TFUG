def inject_ai7_feedback(nodes, profiles):
    for node in nodes:
        if node.get("node_type") == "profile":
            org_id = node["node_id"].split("::")[-1]
            profile = profiles.get(org_id)
            if profile:
                node["score"] = profile.get("total_score")
                node["state"] = profile.get("profile_state")
    return nodes
