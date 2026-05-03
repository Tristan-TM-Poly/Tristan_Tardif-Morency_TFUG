#!/usr/bin/env python3
"""AI-7 Acceleration Engine CI.

Validates acceleration slots and prevents uncontrolled multiplication of agents,
theories, systems, or applications. This is a governance dry-run only.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "AI7_ACCELERATION_ENGINE.md"
SCHEMA = ROOT / "schemas" / "ai7_acceleration_slot.schema.json"
SLOTS = ROOT / "examples" / "acceleration_slots" / "ai7_acceleration_seed_slots.json"

REQUIRED_KEYS = [
    "slot_id",
    "function",
    "domain",
    "packet_type",
    "objective",
    "allowed_outputs",
    "required_gate",
    "max_status_without_external_evidence",
    "blocked_claims",
    "next_least_action",
]

FORBIDDEN_BLOCKLESS = [
    "guaranteed passive income",
    "complete unification",
    "proved tfuga",
    "ai replaces knowledge holders",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    print("[AI7-ACCELERATION-CI] Starting checks")
    for path in [DOC, SCHEMA, SLOTS]:
        if not path.exists():
            fail(f"missing required file: {path}")
        ok(f"found {path.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8").lower()
    for token in ["humanreviewgate", "evidencegate", "dct++", "reproduction throttle", "blocked acceleration"]:
        if token not in doc:
            fail(f"acceleration doc missing token: {token}")
    ok("acceleration doc tokens")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for key in REQUIRED_KEYS:
        if key not in required:
            fail(f"schema missing required field: {key}")
    ok("schema required fields")

    slots = json.loads(SLOTS.read_text(encoding="utf-8"))
    if not isinstance(slots, list) or not slots:
        fail("slots file must contain non-empty list")
    ids = set()
    for slot in slots:
        for key in REQUIRED_KEYS:
            if key not in slot:
                fail(f"slot missing key {key}: {slot}")
        if slot["slot_id"] in ids:
            fail(f"duplicate slot_id: {slot['slot_id']}")
        ids.add(slot["slot_id"])
        blocked = "\n".join(slot.get("blocked_claims", [])).lower()
        for phrase in FORBIDDEN_BLOCKLESS:
            if phrase in slot.get("objective", "").lower() and phrase not in blocked:
                fail(f"risky objective phrase not blocked in {slot['slot_id']}: {phrase}")
        ok(f"validated {slot['slot_id']}")

    print("[AI7-ACCELERATION-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
