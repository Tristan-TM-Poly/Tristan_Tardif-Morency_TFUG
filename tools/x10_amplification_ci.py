#!/usr/bin/env python3
"""TFUGA x10 Amplification CI.

Validates x10 amplification artifacts. It ensures amplification means more
packets, gates, tests, feedback, visibility, reuse, and crystallization, not
unsupported claims or unsafe external action.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "TFUGA_X10_AMPLIFICATION_PROTOCOL.md"
SCHEMA = ROOT / "schemas" / "tfuga_x10_packet.schema.json"
SAMPLES = ROOT / "samples" / "x10_packets"

REQUIRED_SCHEMA_FIELDS = [
    "amplification_id",
    "source_artifact",
    "axis",
    "factor",
    "allowed_derivatives",
    "required_gate",
    "required_evidence",
    "blocked_claims",
    "risk_control",
    "rollback_path",
    "next_least_action",
]

DOC_TOKENS = [
    "Everything x10 means evidence passports x10",
    "Ten amplification axes",
    "Blocked x10",
    "Multiply capacity, not noise",
]

BLOCKED_CLAIM_TOKENS = [
    "x10 means claims are true",
    "x10 means public launch",
    "x10 means revenue validated",
    "x10 means scientific validation",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    print("[X10-AMPLIFICATION-CI] Starting checks")
    for path in [DOC, SCHEMA]:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        ok(f"found {path.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    for token in DOC_TOKENS:
        if token not in doc:
            fail(f"x10 protocol missing token: {token}")
    ok("x10 protocol tokens")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in required:
            fail(f"x10 schema missing required field: {field}")
    ok("x10 schema required fields")

    if not SAMPLES.exists():
        fail("missing x10 sample directory")
    samples = sorted(SAMPLES.glob("*.json"))
    if not samples:
        fail("no x10 sample packets found")

    for sample in samples:
        data = json.loads(sample.read_text(encoding="utf-8"))
        for field in REQUIRED_SCHEMA_FIELDS:
            if field not in data:
                fail(f"{sample.name} missing field: {field}")
        if int(data.get("factor", 0)) > 10:
            fail(f"{sample.name} factor exceeds 10")
        blocked = "\n".join(data.get("blocked_claims", [])).lower()
        for token in BLOCKED_CLAIM_TOKENS:
            if token not in blocked:
                fail(f"{sample.name} missing blocked claim token: {token}")
        ok(f"validated {sample.name}")

    print("[X10-AMPLIFICATION-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
