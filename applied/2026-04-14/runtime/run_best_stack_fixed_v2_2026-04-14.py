from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "applied/2026-04-14/runtime"
ARTIFACTS = RUNTIME / "artifacts"
OUTPUT_PATH = ARTIFACTS / "best_stack_run_report_fixed_v2_2026-04-14.json"


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_best_stack() -> dict[str, Any]:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    fl_emit = load_module(RUNTIME / "emit_fractal_loop_trace_artifact_fixed_2026-04-14.py", "fl_emit_fixed")
    ldk_emit = load_module(RUNTIME / "emit_ldk_bounded_artifact_fixed_2026-04-14.py", "ldk_emit_fixed")
    fl_summary = load_module(RUNTIME / "build_fractal_loop_reviewable_summary_fixed_2026-04-14.py", "fl_summary_fixed")
    ldk_summary = load_module(RUNTIME / "build_ldk_reviewable_summary_fixed_2026-04-14.py", "ldk_summary_fixed")
    raman_summary = load_module(RUNTIME / "build_raman_reviewable_summary_2026-04-14.py", "raman_summary")
    raman_emit = load_module(RUNTIME / "emit_raman_stub_artifact_2026-04-14.py", "raman_emit")
    event_row = load_module(RUNTIME / "emit_event_log_row_2026-04-14.py", "event_row")
    ledger_index = load_module(RUNTIME / "build_generated_ledger_index_2026-04-14.py", "ledger_index")
    coupled_state = load_module(RUNTIME / "build_coupled_frontier_state_2026-04-14.py", "coupled_state")
    frontier_state = load_module(RUNTIME / "update_pilot_frontier_scoreboard_state_2026-04-14.py", "frontier_state")
    consolidated = load_module(RUNTIME / "build_consolidated_frontier_scoreboard_2026-04-14.py", "consolidated")
    raman_stub = load_module(RUNTIME / "emit_raman_stub_artifact_2026-04-14.py", "raman_stub")

    payload = {
        "fractal_loop_artifact": fl_emit.emit_trace_artifact(),
        "ldk_artifact": ldk_emit.emit_artifact(),
        "fractal_loop_reviewable_summary_fixed": fl_summary.build_summary(),
        "ldk_reviewable_summary_fixed": ldk_summary.build_summary(),
        "raman_stub_artifact": raman_stub.emit_raman_stub_artifact(),
        "raman_reviewable_summary": raman_summary.build_summary(),
        "event_log_row": event_row.build_event_row(),
        "generated_ledger_index": ledger_index.build_generated_ledger_index(),
        "coupled_frontier_state": coupled_state.build_coupled_frontier_state(),
        "pilot_frontier_scoreboard_state": frontier_state.build_scoreboard_state(),
        "consolidated_frontier_scoreboard": consolidated.build_scoreboard(),
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_best_stack()
    print(json.dumps({
        "fractal_loop_bounded": result["fractal_loop_artifact"]["result"]["bounded"],
        "ldk_admissible": result["ldk_artifact"]["result"]["admissible"],
        "report": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))
