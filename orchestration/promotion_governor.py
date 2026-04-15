def decide(report):
    decisions = {}
    for agent_id, r in report.items():
        if r["passed"]:
            decisions[agent_id] = "promote"
        else:
            decisions[agent_id] = "review"
    return decisions
