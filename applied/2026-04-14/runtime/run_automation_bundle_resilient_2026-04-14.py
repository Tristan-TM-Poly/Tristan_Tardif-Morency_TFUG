from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "applied/2026-04-14/runtime"
ARTIFACTS = RUNTIME / "artifacts"
JSON_REPORT = ARTIFACTS / "automation_bundle_report_resilient_2026-04-14.json"
MD_REPORT = ARTIFACTS / "automation_bundle_report_resilient_2026-04-14.md"

SCRIPTS = [
    "emit_fractal_loop_trace_artifact_fixed_2026-04-14.py",
    "build_fractal_loop_reviewable_summary_fixed_2026-04-14.py",
    "emit_ldk_bounded_artifact_fixed_2026-04-14.py",
    "build_ldk_reviewable_summary_fixed_2026-04-14.py",
    "emit_raman_stub_artifact_2026-04-14.py",
    "build_raman_reviewable_summary_2026-04-14.py",
    "emit_event_log_row_2026-04-14.py",
    "build_generated_ledger_index_2026-04-14.py",
    "build_coupled_frontier_state_2026-04-14.py",
    "update_pilot_frontier_scoreboard_state_2026-04-14.py",
    "build_consolidated_frontier_scoreboard_2026-04-14.py",
    "build_frontier_governance_digest_generated_2026-04-14.py",
]


def run_script(script_name: str) -> dict:
    script_path = RUNTIME / script_name
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return {
        "script": script_name,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def build_markdown(results: list[dict]) -> str:
    lines = [
        "# AUTOMATION_BUNDLE_REPORT_RESILIENT — Generated Snapshot (2026-04-14)",
        "",
        "| Script | Status | Return code |",
        "|---|---|---:|",
    ]
    for result in results:
        status = "ok" if result["ok"] else "failed"
        lines.append(f"| {result['script']} | {status} | {result['returncode']} |")
    ok_count = sum(1 for r in results if r["ok"])
    fail_count = len(results) - ok_count
    lines += [
        "",
        f"- ok_count: {ok_count}",
        f"- fail_count: {fail_count}",
        "",
        "## Law",
        "The resilient automation report exists to preserve partial progress and make failure visible without collapsing the whole frontier reading.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results = [run_script(name) for name in SCRIPTS]
    payload = {
        "results": results,
        "ok_count": sum(1 for r in results if r["ok"]),
        "fail_count": sum(1 for r in results if not r["ok"]),
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    MD_REPORT.write_text(build_markdown(results), encoding="utf-8")
    print(json.dumps({
        "report_json": str(JSON_REPORT.relative_to(ROOT)),
        "report_md": str(MD_REPORT.relative_to(ROOT)),
        "ok_count": payload["ok_count"],
        "fail_count": payload["fail_count"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
