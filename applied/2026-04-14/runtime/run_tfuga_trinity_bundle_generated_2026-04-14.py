from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "applied/2026-04-14/runtime/artifacts"
OUTPUT_JSON = ARTIFACTS / "tfuga_trinity_bundle_report_generated_2026-04-14.json"
OUTPUT_MD = ARTIFACTS / "tfuga_trinity_bundle_report_generated_2026-04-14.md"

SCRIPTS = [
    "build_ai7_tristan2_upgrade_packet_generated_2026-04-14.py",
    "build_ai7_tristan2_runtime_queue_schema_generated_2026-04-14.py",
    "build_ai7_tristan2_coupled_execution_matrix_generated_2026-04-14.py",
]


def run_script(script_name: str) -> dict:
    script_path = ROOT / "applied/2026-04-14/runtime" / script_name
    proc = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT), capture_output=True, text=True)
    return {
        "script": script_name,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def build_markdown(results: list[dict]) -> str:
    lines = [
        "# TFUGA_TRINITY_BUNDLE_REPORT — Generated Snapshot (2026-04-14)",
        "",
        "| Script | Status | Return code |",
        "|---|---|---:|",
    ]
    for result in results:
        lines.append(f"| {result['script']} | {'ok' if result['ok'] else 'failed'} | {result['returncode']} |")
    lines += [
        "",
        "## Law",
        "The TFUGA trinity bundle exists to keep generation, metabolism, and governance improvements visible from one auditable chain.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results = [run_script(s) for s in SCRIPTS]
    payload = {"results": results}
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(results), encoding="utf-8")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
