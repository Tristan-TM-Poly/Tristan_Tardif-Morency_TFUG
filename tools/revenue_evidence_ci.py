#!/usr/bin/env python3
"""Revenue EvidenceGate governance checks.

Conservative PR-oriented checks for HyperRevenue assets. This script verifies
that the productization package has the minimum review, delivery, support, and
T4 evidence protocol files required before any public launch. It does not create
payment links, publish pages, merge PRs, or claim revenue.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_DIR = ROOT / "products" / "tfuga-hyper-revenue-reactor-v0.8"

REQUIRED_FILES = [
    "README.md",
    "PRODUCT_OMNISPECTRAL_EVIDENCEGATE_STARTER_KIT.md",
    "LANDING_PAGE_COPY.md",
    "LAUNCH_BOARD_30_DAYS.md",
    "REVENUE_CLAIMS_REGISTER_v0_8.md",
    "TFUGA_HYPER_REVENUE_DCTPP_REPORT_v0_8.md",
    "PRICING_EXPERIMENTS.csv",
    "SUPPORT_REFUND_PRIVACY_NOTES.md",
    "DELIVERY_MANIFEST.md",
    "CHECKOUT_T4_EVIDENCE_PROTOCOL.md",
    "CUSTOMER_VALIDATION_BOARD.md",
    "REVENUE_EVIDENCEGATE_V0_9.md",
]

ABSOLUTE_RISK_PHRASES = [
    "guaranteed passive income",
    "automatic revenue without customers",
    "risk-free investment return",
    "autonomous bank",
    "legal/tax compliance already solved",
    "infinite revenue",
]

SAFE_CONTEXT = ["blocked", "does not", "do not", "no ", "not ", "requires", "without", "cannot"]

T4_REQUIRED_MARKERS = [
    "payment processor link",
    "first customer receipt",
    "support contact",
    "privacy/terms checked",
    "human review approval",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read_file(name: str) -> str:
    path = PRODUCT_DIR / name
    if not path.exists():
        fail(f"missing required product file: {name}")
    text = path.read_text(encoding="utf-8")
    ok(f"found {name}")
    return text


def check_risk_context(name: str, text: str) -> None:
    lower = text.lower()
    for phrase in ABSOLUTE_RISK_PHRASES:
        if phrase in lower:
            idx = lower.index(phrase)
            window = lower[max(0, idx - 180): idx + 180]
            if not any(marker in window for marker in SAFE_CONTEXT):
                fail(f"risky phrase lacks safe/blocked context in {name}: {phrase}")


def check_pricing() -> None:
    path = PRODUCT_DIR / "PRICING_EXPERIMENTS.csv"
    with path.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        fail("pricing csv has no rows")
    required_cols = {"tier", "price_usd", "scope"}
    if not required_cols.issubset(rows[0].keys()):
        fail(f"pricing csv missing columns: {required_cols}")
    tiers = {row["tier"] for row in rows}
    for tier in ["Starter", "Pro", "Lab/Education"]:
        if tier not in tiers:
            fail(f"pricing csv missing tier: {tier}")
    ok("pricing csv tiers")


def check_t4_protocol(text: str) -> None:
    lower = text.lower()
    for marker in T4_REQUIRED_MARKERS:
        if marker not in lower:
            fail(f"T4 protocol missing marker: {marker}")
    ok("T4 required markers")


def main() -> int:
    print("[REVENUE-EVIDENCE-CI] Starting checks")
    all_text = ""
    for name in REQUIRED_FILES:
        text = read_file(name)
        check_risk_context(name, text)
        all_text += "\n" + text

    check_pricing()
    check_t4_protocol(read_file("CHECKOUT_T4_EVIDENCE_PROTOCOL.md"))

    if "No passive income is guaranteed" not in all_text and "no guaranteed passive income" not in all_text.lower():
        fail("missing hard law against guaranteed passive income")
    ok("anti-guarantee hard law present")

    if "OmniSpectral EvidenceGate Starter Kit" not in all_text:
        fail("missing selected product name")
    ok("selected product present")

    print("[REVENUE-EVIDENCE-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
