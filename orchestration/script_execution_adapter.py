import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REGISTRY_PATH = Path("orchestration/allowed_scripts.json")
LOG_PATH = Path("out/tfuga/execution_log.jsonl")


def load_registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def is_allowed(script_id, registry):
    return any(s["script_id"] == script_id for s in registry["scripts"])


def get_script(script_id, registry):
    for s in registry["scripts"]:
        if s["script_id"] == script_id:
            return s
    return None


def log_execution(record):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_script(script_id):
    registry = load_registry()

    if not is_allowed(script_id, registry):
        raise RuntimeError(f"Script {script_id} not allowed")

    script = get_script(script_id, registry)
    path = script["path"]

    start = datetime.now(timezone.utc).isoformat()

    try:
        result = subprocess.run([script["runner"], path], capture_output=True, text=True)
        status = "success" if result.returncode == 0 else "failed"
    except Exception as e:
        result = None
        status = "error"

    record = {
        "script_id": script_id,
        "path": path,
        "status": status,
        "timestamp_utc": start,
        "stdout": result.stdout if result else None,
        "stderr": result.stderr if result else None
    }

    log_execution(record)
    return record
