#!/usr/bin/env python3
"""Knowledge Respect governance checks.

Conservative checks for docs/ethics. This script helps reviewers ensure that
community or cultural knowledge references stay public-source, attributed,
permission-aware, and non-extractive. It does not grant permission, publish
content, or promote any claim.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ETHICS_DIR = ROOT / "docs" / "ethics"

REQUIRED_FILES = [
    "KNOWLEDGE_RESPECT_PROTOCOL.md",
    "knowledge_respect.schema.json",
    "CULTURAL_CLAIMS_REGISTER.md",
]

RISK_TERMS = [
    "owns community knowledge",
    "replaces elders",
    "translates everything",
    "commercialized without agreement",
    "documentation alone promotes k4",
    "absorbs",
    "canonizes community knowledge",
]

SAFE_CONTEXT = ["blocked", "do not", "does not", "cannot", "requires", "without permission", "hard law"]

REQUIRED_PROTOCOL_TOKENS = [
    "UseAllowed",
    "K0",
    "K6",
    "BenefitBack",
    "Attribution",
    "ReviewPath",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read_ethics(name: str) -> str:
    path = ETHICS_DIR / name
    if not path.exists():
        fail(f"missing required ethics file: {name}")
    text = path.read_text(encoding="utf-8")
    ok(f"found {name}")
    return text


def check_risk_context(name: str, text: str) -> None:
    lower = text.lower()
    for term in RISK_TERMS:
        if term in lower:
            idx = lower.index(term)
            window = lower[max(0, idx - 220): idx + 220]
            if not any(marker in window for marker in SAFE_CONTEXT):
                fail(f"risk term lacks safe context in {name}: {term}")


def check_schema() -> None:
    schema_path = ETHICS_DIR / "knowledge_respect.schema.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    required = set(schema.get("required", []))
    for field in ["artifact_id", "respect_status", "source_type", "intended_use", "attribution", "review_path", "benefit_back", "blocked_claims"]:
        if field not in required:
            fail(f"schema missing required field: {field}")
    ok("schema required fields")


def main() -> int:
    print("[KNOWLEDGE-RESPECT-CI] Starting checks")
    protocol = ""
    for name in REQUIRED_FILES:
        text = read_ethics(name)
        check_risk_context(name, text)
        if name == "KNOWLEDGE_RESPECT_PROTOCOL.md":
            protocol = text

    for token in REQUIRED_PROTOCOL_TOKENS:
        if token not in protocol:
            fail(f"protocol missing token: {token}")
    ok("protocol tokens")

    check_schema()
    print("[KNOWLEDGE-RESPECT-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
