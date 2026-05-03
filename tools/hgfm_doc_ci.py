#!/usr/bin/env python3
"""HGFM documentation governance checks.

This script is intentionally conservative. It validates documentation structure,
GraphML/JSON parseability, and the presence of EvidenceGate/AntiHype language.
It does not publish, merge, deploy, create payment links, or promote claims.
"""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/hgfm/HGFM_DOCUMENTATION_HYPERGRAPH_MAP.md",
    "docs/hgfm/HGFM_DOC_STYLE_GUIDE.md",
    "docs/hgfm/HGFM_DOCUMENTATION_GRAPH.graphml",
    "docs/hgfm/HGFM_DOCUMENTATION_INDEX.md",
    "docs/hgfm/HGFM_DOCUMENTATION_PROJECTORS.md",
    "docs/hgfm/HGFM_DOCUMENTATION_EVIDENCE_SCHEMA.json",
    "docs/hgfm/HGFM_DOCUMENTATION_CI_PROTOCOL.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/README.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/REVENUE_EVIDENCEGATE_V0_9.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/SUPPORT_REFUND_PRIVACY_NOTES.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/DELIVERY_MANIFEST.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/CHECKOUT_T4_EVIDENCE_PROTOCOL.md",
]

RISK_PHRASES = [
    "guaranteed passive income",
    "validated superconductivity",
    "autonomous lab control",
    "risk-free return",
    "proven physical effect",
    "infinite revenue",
]

SAFE_CONTEXT_MARKERS = [
    "blocked",
    "does not",
    "do not",
    "no guaranteed",
    "cannot",
    "requires",
    "without evidence",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def read_rel(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"missing required file: {path}")
    return full.read_text(encoding="utf-8")


def check_status_line(path: str, text: str) -> None:
    if path.endswith(".md") and "Status:" not in text[:1200]:
        fail(f"missing Status line near top: {path}")


def check_risky_language(path: str, text: str) -> None:
    lower = text.lower()
    for phrase in RISK_PHRASES:
        if phrase in lower:
            idx = lower.index(phrase)
            window = lower[max(0, idx - 220): idx + 220]
            if not any(marker in window for marker in SAFE_CONTEXT_MARKERS):
                fail(f"risky phrase lacks blocked/safe context in {path}: {phrase}")


def main() -> int:
    print("[HGFM-DOC-CI] Starting governance checks")

    for rel in REQUIRED_FILES:
        text = read_rel(rel)
        check_status_line(rel, text)
        check_risky_language(rel, text)
        print(f"[OK] {rel}")

    schema_path = ROOT / "docs/hgfm/HGFM_DOCUMENTATION_EVIDENCE_SCHEMA.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    required = set(schema.get("required", []))
    for key in ["artifact_id", "status", "claim_class", "claims", "evidence", "missing_evidence", "blocked_claims"]:
        if key not in required:
            fail(f"schema missing required field: {key}")
    print("[OK] evidence schema required fields")

    graph_path = ROOT / "docs/hgfm/HGFM_DOCUMENTATION_GRAPH.graphml"
    ET.parse(graph_path)
    print("[OK] GraphML parse")

    ci_protocol = read_rel("docs/hgfm/HGFM_DOCUMENTATION_CI_PROTOCOL.md")
    for token in ["claim-ledger-check", "graphml-smoke-test", "blocked-claim-scan"]:
        if token not in ci_protocol:
            fail(f"CI protocol missing token: {token}")
    print("[OK] CI protocol gates")

    print("[HGFM-DOC-CI] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
