from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "applied/2026-04-14/runtime/LDK_BOUNDED_EXECUTABLE_PLACEHOLDER_2026-04-14.py"
OUTPUT_DIR = ROOT / "applied/2026-04-14/runtime/artifacts"
OUTPUT_PATH = OUTPUT_DIR / "ldk_bounded_artifact_fixed_2026-04-14.json"


def load_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("ldk_bounded_placeholder_fixed", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load source module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def emit_artifact() -> dict[str, Any]:
    module = load_source_module()
    result = module.run_ldk_bounded_example()
    payload = {
        "artifact_type": "ldk_bounded_example_fixed",
        "source": str(SOURCE.relative_to(ROOT)),
        "result": result,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = emit_artifact()
    print(json.dumps(payload, indent=2))
