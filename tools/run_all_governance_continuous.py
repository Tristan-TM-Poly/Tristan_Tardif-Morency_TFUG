#!/usr/bin/env python3
"""Run all TFUGA governance gates continuously or on demand.

This script executes every available governance check in a deterministic order.
It is safe-by-design: it does not merge, deploy, publish, create payment links,
contact third parties, spend money, access unauthorized data, or promote claims.
It only runs local/read-only validation gates and prints a summary.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTERVAL_SECONDS = 3600

GATES = [
    ("HGFMDocGate", "tools/hgfm_doc_ci.py"),
    ("RevenueEvidenceGate", "tools/revenue_evidence_ci.py"),
    ("KnowledgeRespectGate", "tools/knowledge_respect_ci.py"),
    ("UnifiedGovernanceGate", "tools/tfuga_unified_governance_ci.py"),
    ("AI7AgentFactoryGate", "tools/ai7_agent_factory_ci.py"),
    ("AI7AccelerationGate", "tools/ai7_acceleration_ci.py"),
    ("ClaimRouterGate", "tools/claim_router_ci.py"),
]

OUTPUT_DIR = ROOT / "outputs" / "governance"
OUTPUT_FILE = OUTPUT_DIR / "continuous_governance_status.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_gate(name: str, rel_script: str) -> dict:
    script = ROOT / rel_script
    started = utc_now()
    if not script.exists():
        return {
            "gate": name,
            "script": rel_script,
            "status": "missing",
            "started_at": started,
            "ended_at": utc_now(),
            "returncode": None,
            "stdout_tail": "",
            "stderr_tail": f"missing script: {rel_script}",
        }

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return {
        "gate": name,
        "script": rel_script,
        "status": "pass" if result.returncode == 0 else "fail",
        "started_at": started,
        "ended_at": utc_now(),
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    }


def run_once() -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [run_gate(name, script) for name, script in GATES]
    summary = {
        "generated_at": utc_now(),
        "mode": "single-pass",
        "status": "pass" if all(r["status"] == "pass" for r in results) else "fail",
        "pass_count": sum(1 for r in results if r["status"] == "pass"),
        "fail_count": sum(1 for r in results if r["status"] == "fail"),
        "missing_count": sum(1 for r in results if r["status"] == "missing"),
        "gates": results,
        "hard_law": "Continuous governance runs checks only. It does not merge, deploy, publish, spend, create payment links, or promote claims.",
    }
    OUTPUT_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def print_summary(summary: dict) -> None:
    print(f"[TFUGA-CONTINUOUS] {summary['generated_at']} status={summary['status']} pass={summary['pass_count']} fail={summary['fail_count']} missing={summary['missing_count']}")
    for gate in summary["gates"]:
        print(f"- {gate['gate']}: {gate['status']} ({gate['script']})")
    print(f"[TFUGA-CONTINUOUS] wrote {OUTPUT_FILE.relative_to(ROOT)}")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run all TFUGA governance gates.")
    parser.add_argument("--continuous", action="store_true", help="Repeat forever until interrupted.")
    parser.add_argument("--interval-seconds", type=int, default=DEFAULT_INTERVAL_SECONDS, help="Delay between continuous runs.")
    args = parser.parse_args()

    if args.continuous:
        print("[TFUGA-CONTINUOUS] continuous mode started. Stop with Ctrl+C.")
        while True:
            summary = run_once()
            print_summary(summary)
            time.sleep(max(60, args.interval_seconds))
    else:
        summary = run_once()
        print_summary(summary)
        return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
