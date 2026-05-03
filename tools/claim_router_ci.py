#!/usr/bin/env python3
"""TFUGA Claim Router CI.

Validates that claims are routed to the correct evidence gates. This is a
governance dry-run. It does not promote, publish, deploy, spend, merge, or
claim truth.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "tools" / "claim_router.py"
DOC = ROOT / "docs" / "governance" / "TFUGA_CLAIM_ROUTER.md"
SCHEMA = ROOT / "schemas" / "tfuga_claim_route.schema.json"
SAMPLES = ROOT / "samples" / "claim_routes"

EXPECTED = [
    ("Raman spectrum validates material performance", "science", "S3"),
    ("OmniSpectral Starter Kit generated passive income", "revenue", "T3"),
    ("First Nations knowledge can be translated and used", "cultural", "K3"),
    ("Deploy to Vercel and create Stripe payment link", "deployment", "T3"),
    ("This Python package has tests and CI", "software", "S3"),
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def run_route(claim: str) -> dict:
    result = subprocess.run([sys.executable, str(ROUTER), claim], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        fail(f"router failed for claim: {claim}\n{result.stderr}")
    return json.loads(result.stdout)


def main() -> int:
    print("[CLAIM-ROUTER-CI] Starting checks")
    for path in [ROUTER, DOC, SCHEMA]:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        ok(f"found {path.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8").lower()
    for token in ["claimroute", "requiredgate", "maxstatus", "missingevidence", "no claim reaches promotion directly"]:
        if token not in doc.replace(" ", ""):
            fail(f"claim router doc missing token: {token}")
    ok("claim router doc tokens")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for key in ["claim_id", "claim_text", "claim_type", "required_gate", "missing_evidence", "blocked_claims", "human_review_required"]:
        if key not in required:
            fail(f"schema missing required field: {key}")
    ok("claim route schema required fields")

    for claim, expected_type, expected_status in EXPECTED:
        packet = run_route(claim)
        if packet["claim_type"] != expected_type:
            fail(f"expected {expected_type}, got {packet['claim_type']} for {claim}")
        if packet["max_status_without_external_evidence"] != expected_status:
            fail(f"expected {expected_status}, got {packet['max_status_without_external_evidence']} for {claim}")
        if not packet.get("human_review_required", False):
            fail(f"human review not required for {claim}")
        ok(f"routed {expected_type}: {claim}")

    if SAMPLES.exists():
        for sample in sorted(SAMPLES.glob("*.json")):
            data = json.loads(sample.read_text(encoding="utf-8"))
            if "claim_type" not in data or "required_gate" not in data:
                fail(f"bad sample packet: {sample.name}")
            ok(f"sample packet {sample.name}")

    print("[CLAIM-ROUTER-CI] All checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
