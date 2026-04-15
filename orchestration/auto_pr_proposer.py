def propose_pr(decisions):
    proposals = []
    for agent_id, decision in decisions.items():
        if decision == "promote":
            proposals.append({
                "agent": agent_id,
                "action": "open_pr",
                "status": "proposed"
            })
        else:
            proposals.append({
                "agent": agent_id,
                "action": "review_required",
                "status": "blocked"
            })
    return proposals
