from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any


def execute_merge(plan: dict[str, Any], output_dir: str) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    results = []
    for action in plan.get("actions", []):
        if action.get("action") == "extract":
            path = Path(action["path"])
            try:
                with zipfile.ZipFile(path, 'r') as z:
                    z.extractall(out / path.stem)
                results.append({"path": str(path), "status": "extracted"})
            except Exception as e:
                results.append({"path": str(path), "status": "error", "error": str(e)})

    return {
        "output_dir": str(out),
        "results": results
    }
