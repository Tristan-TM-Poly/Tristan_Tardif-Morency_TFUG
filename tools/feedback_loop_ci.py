#!/usr/bin/env python3
"""Human + AI Feedback Loop CI.

Validates feedback and interaction artifacts. This is review-oriented: it does
not merge, deploy, publish, contact reviewers, claim evidence, or promote status.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/feedback/HUMAN_AI_FEEDBACK_LOOP.md",
    "schemas/feedback_packet.schema.json",
    "docs/feedback/FEEDBACK_REVIEW_BOARD.md",
    "docs/feedback/HUMAN_AI_INTERACTION_PROTOCOL.md",
]

REQUIRED_LOOP_TOKENS = [
    "Feedback improves direction",
    "Evidence promotes status",
    "Collect",
    "Classify",
    "Patch",
    "Test",
    "Review",
]

REQUIRED_SCHEMA_FIELDS = [
    "feedback_id",
    "source_type",
    "summary",
    "class",
    "severity",
    "suggested_patch",
    "required_gate",
    "evidence_needed",
    "status",
    "next_least_action",
]

BLOCKED_INTERACTION_TOKENS = [
    "merge",
    "deploy",
    "publish externally",
    "create payment links",
    "contact third parties",
    "claim revenue",
    "claim scientific validation",
    "claim cultural/community permission",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read_rel(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"missing required file: {path}")
    ok(f"found {path}")
    return full.read_text(encoding="utf-8")


def main() -> int:
    print("[FEEDBACK-LOOP-CI] Starting checks")
    texts = {path: read_rel(path) for path in REQUIRED_FILES}

    loop = texts["docs/feedback/HUMAN_AI_FEEDBACK_LOOP.md"]
    for token in REQUIRED_LOOP_TOKENS:
        if token not in loop:
            fail(f"feedback loop missing token: {token}")
    ok("feedback loop tokens")

    schema = json.loads(texts["schemas/feedback_packet.schema.json"])
    required = set(schema.get("required", []))
    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in required:
            fail(f"feedback schema missing required field: {field}")
    ok("feedback schema required fields")

    board = texts["docs/feedback/FEEDBACK_REVIEW_BOARD.md"]
    for token in ["FB-001", "FB-006", "Severity scale", "Feedback-to-patch law"]:
        if token not in board:
            fail(f"feedback board missing token: {token}")
    ok("feedback board tokens")

    interaction = texts["docs/feedback/HUMAN_AI_INTERACTION_PROTOCOL.md"]
    lower = interaction.lower()
    for token in ["human asks, ai structures", "ai critiques, human decides", "human approves external action"]:
        if token not in lower:
            fail(f"interaction protocol missing token: {token}")
    for token in BLOCKED_INTERACTION_TOKENS:
        if token.lower() not in lower:
            fail(f"interaction protocol missing blocked action token: {token}")
    ok("interaction protocol tokens")

    print("[FEEDBACK-LOOP-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
