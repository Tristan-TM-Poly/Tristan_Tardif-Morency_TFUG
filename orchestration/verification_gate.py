def verify_results(results):
    report = {}
    for agent_id, tasks in results.items():
        report[agent_id] = {
            "passed": all(t["status"] == "executed" for t in tasks),
            "task_count": len(tasks)
        }
    return report
