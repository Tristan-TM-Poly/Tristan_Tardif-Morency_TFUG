def execute_tasks(assignments):
    results = {}
    for agent_id, tasks in assignments.items():
        results[agent_id] = []
        for task in tasks:
            results[agent_id].append({
                "task": task,
                "status": "executed"
            })
    return results
