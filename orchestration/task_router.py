def route_tasks(task_graph, agents):
    assignments = {}
    for task in task_graph:
        role = task.get("role")
        for agent in agents:
            if agent["role"] == role:
                assignments.setdefault(agent["agent_id"], []).append(task)
    return assignments
