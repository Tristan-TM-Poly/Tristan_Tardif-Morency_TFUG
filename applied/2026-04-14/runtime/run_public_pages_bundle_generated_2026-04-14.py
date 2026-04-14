from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "applied/2026-04-14/runtime"
ARTIFACTS = RUNTIME / "artifacts"
JSON_REPORT = ARTIFACTS / "public_pages_bundle_report_generated_2026-04-14.json"
MD_REPORT = ARTIFACTS / "public_pages_bundle_report_generated_2026-04-14.md"

SCRIPTS = [
    "build_auto_generator_module_catalog_generated_2026-04-14.py",
    "build_auto_generator_integration_map_generated_2026-04-14.py",
    "run_tfuga_auto_generative_web_bundle_generated_2026-04-14.py",
]


def run_script(script_name: str) -> dict:
    script_path = RUNTIME / script_name
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
        "# PUBLIC_PAGES_BUNDLE_REPORT — Generated Snapshot (2026-04-14)",
        "",
        "| Script | Status | Return code |",
        "|---|---|---:|",
    ]
    for result in results:
        lines.append(f"| {result['script']} | {'ok' if result['ok'] else 'failed'} | {result['returncode']} |")
    lines += [
        "",
        "## Law",
        "This public pages bundle exists to keep demos, collaborations, and generative page surfaces auditable from one chain.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results = [run_script(s) for s in SCRIPTS]
    payload = {"results": results}
    JSON_REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    MD_REPORT.write_text(build_markdown(results), encoding="utf-8")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
