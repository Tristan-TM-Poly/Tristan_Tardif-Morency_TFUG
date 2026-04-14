from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "applied/2026-04-14/runtime/FRACTAL_LOOP_EXECUTABLE_TRACE_PLACEHOLDER_2026-04-14.py"
OUTPUT_DIR = ROOT / "applied/2026-04-14/runtime/artifacts"
OUTPUT_PATH = OUTPUT_DIR / "fractal_loop_trace_artifact_2026-04-14.json"


def load_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("fractal_loop_trace_placeholder", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load source module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def emit_trace_artifact() -> dict[str, Any]:
    module = load_source_module()
    result = module.run_reduced_trace()
    payload = {
        "artifact_type": "fractal_loop_reduced_trace",
        "source": str(SOURCE.relative_to(ROOT)),
        "result": result.to_dict(),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = emit_trace_artifact()
    print(json.dumps(payload, indent=2))
