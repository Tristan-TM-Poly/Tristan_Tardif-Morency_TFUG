from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "applied/2026-04-14/runtime"
ARTIFACTS = RUNTIME / "artifacts"
JSON_REPORT = ARTIFACTS / "reporting_bundle_report_generated_2026-04-14.json"
MD_REPORT = ARTIFACTS / "reporting_bundle_report_generated_2026-04-14.md"

SCRIPTS = [
    "run_improvement_and_writing_bundle_2026-04-14.py",
    "build_auto_technical_report_generated_2026-04-14.py",
    "build_ieee_latex_stub_extended_generated_2026-04-14.py",
    "build_change_digest_generated_2026-04-14.py",
    "build_closed_loop_improvement_actions_generated_2026-04-14.py",
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
        "# REPORTING_BUNDLE_REPORT — Generated Snapshot (2026-04-14)",
        "",
        "| Script | Status | Return code |",
        "|---|---|---:|",
    ]
    for result in results:
        status = "ok" if result["ok"] else "failed"
        lines.append(f"| {result['script']} | {status} | {result['returncode']} |")
    lines += [
        "",
        "## Law",
        "This reporting bundle exists to transform automation state into readable technical reporting, writing-ready outputs, and next-step improvement actions.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results = [run_script(name) for name in SCRIPTS]
    payload = {"results": results}
    JSON_REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    MD_REPORT.write_text(build_markdown(results), encoding="utf-8")
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({
        "report_json": str(JSON_REPORT.relative_to(ROOT)),
        "report_md": str(MD_REPORT.relative_to(ROOT)),
        "failed_count": len(failed),
    }, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
