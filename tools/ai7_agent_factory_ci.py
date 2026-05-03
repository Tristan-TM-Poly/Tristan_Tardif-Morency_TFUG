#!/usr/bin/env python3
"""AI-7 Governed Agent Factory CI.

Validates agent specs and prevents uncontrolled autonomy claims. This script is
review-oriented. It does not spawn real agents, call external APIs, deploy,
spend money, publish, or bypass human review.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ai7_agent_spec.schema.json"
EXAMPLES = ROOT / "examples" / "ai7_agent_specs"
DOC = ROOT / "docs" / "governance" / "AI7_GOVERNED_AGENT_FACTORY.md"

REQUIRED_KEYS = [
    "agent_id",
    "role",
    "domain",
    "allowed_actions",
    "blocked_actions",
    "inputs",
    "outputs",
    "required_evidence",
    "risk_level",
    "human_review_required",
]

FORBIDDEN_ALLOWED_ACTIONS = [
    "auto-merge",
    "spend money",
    "publish unsupported claims",
    "bypass evidencegate",
    "access unauthorized data",
    "hide actions",
    "remove guardrails",
]

REQUIRED_BLOCKED_ACTIONS = [
    "auto-merge",
    "spend money",
    "publish unsupported claims",
    "bypass EvidenceGate",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    print("[AI7-AGENT-FACTORY-CI] Starting checks")
    if not SCHEMA.exists():
        fail("missing schema")
    if not DOC.exists():
        fail("missing agent factory doc")
    if not EXAMPLES.exists():
        fail("missing examples directory")

    doc_text = DOC.read_text(encoding="utf-8").lower()
    for token in ["humanreviewgate", "evidencegate", "rollback", "forbidden spawns", "status ceiling"]:
        if token not in doc_text:
            fail(f"agent factory doc missing token: {token}")
    ok("agent factory doc tokens")

    specs = sorted(EXAMPLES.glob("*.agent.json"))
    if not specs:
        fail("no agent specs found")

    for spec_path in specs:
        data = json.loads(spec_path.read_text(encoding="utf-8"))
        for key in REQUIRED_KEYS:
            if key not in data:
                fail(f"{spec_path.name} missing key: {key}")
        allowed = [str(x).lower() for x in data.get("allowed_actions", [])]
        blocked = [str(x) for x in data.get("blocked_actions", [])]
        blocked_lower = [x.lower() for x in blocked]
        for forbidden in FORBIDDEN_ALLOWED_ACTIONS:
            if forbidden in allowed:
                fail(f"{spec_path.name} allows forbidden action: {forbidden}")
        for required in REQUIRED_BLOCKED_ACTIONS:
            if required.lower() not in blocked_lower:
                fail(f"{spec_path.name} does not block required action: {required}")
        if not data.get("human_review_required", False):
            fail(f"{spec_path.name} must require human review")
        ok(f"validated {spec_path.name}")

    print("[AI7-AGENT-FACTORY-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
