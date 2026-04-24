from orchestration.script_execution_adapter import run_script


def execute_agent_task(task):
    script_id = task.get("script_id")
    if not script_id:
        return {"status": "no_script"}

    result = run_script(script_id)
    return result
