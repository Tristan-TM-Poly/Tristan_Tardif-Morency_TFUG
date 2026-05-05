#!/usr/bin/env python3
"""Generate TFUGA governance dashboard.

Runs the full governance suite once, reads the status JSON, and emits a
human-readable dashboard. This is a reporting tool only. It does not merge,
deploy, publish, spend, create payment links, contact third parties, access
unauthorized data, or promote claims.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "outputs" / "governance" / "continuous_governance_status.json"
DASHBOARD_PATH = ROOT / "outputs" / "governance" / "TFUGA_GOVERNANCE_DASHBOARD.md"
DASHBOARD_JSON_PATH = ROOT / "outputs" / "governance" / "governance_dashboard.json"

STATUS_EXPLAINERS = {
    "pass": "Gate passed local/read-only governance checks.",
    "fail": "Gate failed and requires review before promotion.",
    "missing": "Gate script or artifact is missing.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_all_gates() -> None:
    runner = ROOT / "tools" / "run_all_governance_continuous.py"
    if not runner.exists():
        raise SystemExit("Missing tools/run_all_governance_continuous.py")
    subprocess.run([sys.executable, str(runner)], cwd=ROOT, check=False)


def load_status() -> dict:
    if not STATUS_PATH.exists():
        raise SystemExit(f"Missing status file: {STATUS_PATH}")
    return json.loads(STATUS_PATH.read_text(encoding="utf-8"))


def readiness_score(status: dict) -> int:
    gates = status.get("gates", [])
    if not gates:
        return 0
    passed = sum(1 for g in gates if g.get("status") == "pass")
    return round(100 * passed / len(gates))


def next_actions(status: dict) -> list[str]:
    gates = status.get("gates", [])
    failed = [g for g in gates if g.get("status") == "fail"]
    missing = [g for g in gates if g.get("status") == "missing"]
    actions: list[str] = []
    if missing:
        actions.append("Create or restore missing governance scripts before promotion.")
    if failed:
        actions.append("Inspect failing gate stdout/stderr tails and patch the related docs/schemas/tools.")
    if not failed and not missing:
        actions.append("Keep PR in human review; do not promote claims without external evidence.")
        actions.append("For T4, collect a real receipt/sponsor log plus delivery/support/privacy evidence.")
        actions.append("For S4, collect real instrument data, metadata, controls, calibration, replicates, uncertainty, and hashes.")
        actions.append("For K4, collect appropriate community or knowledge-holder review/permission path.")
    return actions


def render_markdown(status: dict) -> str:
    score = readiness_score(status)
    lines = [
        "# TFUGA Governance Dashboard",
        "",
        "Status: S3/T3/K3 dashboard artifact.",
        "",
        f"Generated at: `{utc_now()}`",
        f"Source status generated at: `{status.get('generated_at', 'unknown')}`",
        f"Global gate status: `{status.get('status', 'unknown')}`",
        f"Readiness score: `{score}/100`",
        "",
        "## Hard law",
        "",
        "This dashboard reports governance state only. It does not merge, deploy, publish, spend, create payment links, contact third parties, access unauthorized data, or promote claims.",
        "",
        "## Gates",
        "",
        "| Gate | Status | Script | Meaning |",
        "|---|---:|---|---|",
    ]
    for gate in status.get("gates", []):
        gstatus = gate.get("status", "unknown")
        lines.append(f"| {gate.get('gate')} | `{gstatus}` | `{gate.get('script')}` | {STATUS_EXPLAINERS.get(gstatus, 'Needs review.')} |")
    lines.extend([
        "",
        "## Counts",
        "",
        f"- Passed: `{status.get('pass_count', 0)}`",
        f"- Failed: `{status.get('fail_count', 0)}`",
        f"- Missing: `{status.get('missing_count', 0)}`",
        "",
        "## Status ceilings",
        "",
        "- Science/software/docs: S3 maximum without real experimental evidence.",
        "- Revenue/product: T3 maximum without a real receipt or sponsor log.",
        "- Cultural/community knowledge: K3 maximum without appropriate review or permission.",
        "",
        "## Next least-action route",
        "",
    ])
    for action in next_actions(status):
        lines.append(f"- {action}")
    lines.extend([
        "",
        "## Promotion locks",
        "",
        "- No proof, no scientific promotion.",
        "- No receipt, no revenue promotion.",
        "- No permission/review, no cultural/community-knowledge promotion.",
        "- No explicit approval and rollback, no deployment/external action promotion.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    run_all_gates()
    status = load_status()
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    dashboard_md = render_markdown(status)
    DASHBOARD_PATH.write_text(dashboard_md + "\n", encoding="utf-8")
    payload = {
        "generated_at": utc_now(),
        "readiness_score": readiness_score(status),
        "status": status.get("status", "unknown"),
        "counts": {
            "pass": status.get("pass_count", 0),
            "fail": status.get("fail_count", 0),
            "missing": status.get("missing_count", 0),
        },
        "next_actions": next_actions(status),
        "source_status_path": str(STATUS_PATH.relative_to(ROOT)),
        "dashboard_markdown_path": str(DASHBOARD_PATH.relative_to(ROOT)),
        "hard_law": "Dashboard reports governance only; it does not promote claims or perform external actions.",
    }
    DASHBOARD_JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[TFUGA-DASHBOARD] wrote {DASHBOARD_PATH.relative_to(ROOT)}")
    print(f"[TFUGA-DASHBOARD] wrote {DASHBOARD_JSON_PATH.relative_to(ROOT)}")
    return 0 if status.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
