#!/usr/bin/env python3
"""Auto-governed revenue and purchase CI.

Validates transaction governance artifacts. This is a review and blocking gate.
It does not spend, buy, sell, refund, subscribe, create payment links, contact
third parties, collect payments, or promote revenue claims.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "AUTO_GOVERNED_REVENUE_AND_PURCHASES.md"
SCHEMA = ROOT / "schemas" / "transaction_governance_packet.schema.json"
SAMPLES = ROOT / "samples" / "transactions"

REQUIRED_DOC_TOKENS = [
    "AI may analyze, route, score, draft, compare, warn, and log",
    "AI may not spend",
    "TransactionAllowed",
    "Revenue tiers",
    "Spending tiers",
    "Blocked actions",
]

REQUIRED_SCHEMA_FIELDS = [
    "transaction_id",
    "transaction_type",
    "status",
    "tier",
    "description",
    "budget_or_price",
    "required_approval",
    "evidence_needed",
    "risk_review",
    "blocked_actions",
    "ledger_path",
    "next_least_action",
]

MUST_BLOCK = [
    "create payment link automatically",
    "charge buyer automatically",
    "claim T4 without receipt",
    "promise income",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    print("[TRANSACTION-GOVERNANCE-CI] Starting checks")
    for path in [DOC, SCHEMA]:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        ok(f"found {path.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    for token in REQUIRED_DOC_TOKENS:
        if token not in doc:
            fail(f"transaction governance doc missing token: {token}")
    ok("transaction governance doc tokens")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in required:
            fail(f"transaction schema missing required field: {field}")
    ok("transaction schema required fields")

    if not SAMPLES.exists():
        fail("missing transactions sample directory")
    samples = sorted(SAMPLES.glob("*.json"))
    if not samples:
        fail("no transaction sample packets found")

    for sample in samples:
        data = json.loads(sample.read_text(encoding="utf-8"))
        for field in REQUIRED_SCHEMA_FIELDS:
            if field not in data:
                fail(f"{sample.name} missing field: {field}")
        blocked = "\n".join(data.get("blocked_actions", [])).lower()
        for token in MUST_BLOCK:
            if token.lower() not in blocked:
                fail(f"{sample.name} missing blocked action: {token}")
        if data.get("status") == "executed":
            fail(f"{sample.name} cannot be executed in governance sample")
        ok(f"validated {sample.name}")

    print("[TRANSACTION-GOVERNANCE-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
