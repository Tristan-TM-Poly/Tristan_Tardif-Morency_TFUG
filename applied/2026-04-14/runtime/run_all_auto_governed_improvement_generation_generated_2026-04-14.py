from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "applied/2026-04-14/runtime"
ARTIFACTS = RUNTIME / "artifacts"
JSON_REPORT = ARTIFACTS / "run_all_auto_governed_improvement_generation_report_generated_2026-04-14.json"
MD_REPORT = ARTIFACTS / "run_all_auto_governed_improvement_generation_report_generated_2026-04-14.md"

SCRIPTS = [
    "build_exponential_improvement_axes_generated_2026-04-14.py",
    "build_auto_governed_expansion_dashboard_generated_2026-04-14.py",
    "run_abcd_synergy_integration_bundle_generated_2026-04-14.py",
    "run_tfuga_auto_generative_web_bundle_generated_2026-04-14.py",
    "run_public_pages_bundle_generated_2026-04-14.py",
    "run_tfuga_public_visualizers_bundle_generated_2026-04-14.py",
    "run_tfuga_public_interactive_trinity_bundle_generated_2026-04-14.py",
    "run_tfuga_life_projects_aibots_bundle_generated_2026-04-14.py",
    "run_tfuga_edugame_hypergraph_bundle_generated_2026-04-14.py",
    "run_tfuga_trinity_packet_family_bundle_generated_2026-04-14.py",
    "run_ai7_tristan2_corridor_bundle_generated_2026-04-14.py",
    "run_ai7_tristan2_v6_bundle_generated_2026-04-14.py",
    "run_publication_prep_bundle_generated_2026-04-14.py",
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
        "# RUN_ALL_AUTO_GOVERNED_IMPROVEMENT_GENERATION_REPORT — Generated Snapshot (2026-04-14)",
        "",
        "| Script | Status | Return code |",
        "|---|---|---:|",
    ]
    for result in results:
        lines.append(f"| {result['script']} | {'ok' if result['ok'] else 'failed'} | {result['returncode']} |")
    ok_count = sum(1 for r in results if r['ok'])
    fail_count = len(results) - ok_count
    lines += [
        "",
        f"- ok_count: {ok_count}",
        f"- fail_count: {fail_count}",
        "",
        "## Law",
        "This run-all bundle is valid only if broad generation remains explicitly governed, reviewable, and rollback-compatible.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results = [run_script(s) for s in SCRIPTS]
    payload = {
        "results": results,
        "ok_count": sum(1 for r in results if r['ok']),
        "fail_count": sum(1 for r in results if not r['ok']),
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    MD_REPORT.write_text(build_markdown(results), encoding='utf-8')
    return 0 if payload['fail_count'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
