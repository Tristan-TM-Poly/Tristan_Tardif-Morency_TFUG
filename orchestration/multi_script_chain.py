from orchestration.script_execution_adapter import run_script


def run_chain(script_ids):
    results = []
    for sid in script_ids:
        result = run_script(sid)
        results.append(result)
        if result.get("status") != "success":
            break
    return results
