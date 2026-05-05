#!/usr/bin/env python3
"""Reusable Disruption Engine CI.

Validates disruption packets. This gate ensures disruption means measurable,
reusable, evidence-routed workflow improvement, not louder claims.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "REVOLUTIONARY_REUSABLE_DISRUPTION_ENGINE.md"
SCHEMA = ROOT / "schemas" / "disruption_packet.schema.json"
SAMPLES = ROOT / "samples" / "disruption_packets"

REQUIRED_FIELDS = [
    "disruption_id",
    "name",
    "old_workflow",
    "new_workflow",
    "obsolete_assumption",
    "bridge_object",
    "advantage_metric",
    "minimum_demo",
    "required_gate",
    "required_evidence",
    "reuse_kernel",
    "feedback_plan",
    "blocked_claims",
    "rollback_path",
    "status",
    "next_least_action",
]

DOC_TOKENS = [
    "Disruption is not a louder claim",
    "seven conditions",
    "DisruptionScore",
    "Blocked disruption claims",
    "reusable, tested, evidence-routed improvement path",
]

MUST_BLOCK = [
    "guaranteed revenue",
    "scientific validation without real data",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    print("[DISRUPTION-ENGINE-CI] Starting checks")
    for path in [DOC, SCHEMA]:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        ok(f"found {path.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    for token in DOC_TOKENS:
        if token not in doc:
            fail(f"disruption engine doc missing token: {token}")
    ok("disruption engine doc tokens")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for field in REQUIRED_FIELDS:
        if field not in required:
            fail(f"schema missing required field: {field}")
    ok("schema required fields")

    samples = sorted(SAMPLES.glob("*.json")) if SAMPLES.exists() else []
    if not samples:
        fail("no disruption sample packets found")

    for sample in samples:
        data = json.loads(sample.read_text(encoding="utf-8"))
        for field in REQUIRED_FIELDS:
            if field not in data:
                fail(f"{sample.name} missing field: {field}")
        blocked = "\n".join(data.get("blocked_claims", [])).lower()
        for token in MUST_BLOCK:
            if token not in blocked:
                fail(f"{sample.name} missing blocked claim: {token}")
        if "gate" not in data.get("required_gate", "").lower():
            fail(f"{sample.name} required_gate should contain a gate")
        ok(f"validated {sample.name}")

    print("[DISRUPTION-ENGINE-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
