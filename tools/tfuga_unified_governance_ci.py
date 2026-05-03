#!/usr/bin/env python3
"""TFUGA unified governance gate.

Runs conservative checks across the HGFM documentation layer, HyperRevenue
productization layer, and Knowledge Respect layer. This is a review assistant,
not an autonomous publisher. It does not merge PRs, deploy, create payment
links, upload Drive files, or promote scientific/revenue/cultural claims.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORKFLOWS = [
    ".github/workflows/hgfm_doc_governance.yml",
    ".github/workflows/revenue_evidence_governance.yml",
    ".github/workflows/knowledge_respect_governance.yml",
]

FORBIDDEN_WORKFLOW_TOKENS = [
    "contents: write",
    "pull-requests: write",
    "actions: write",
    "auto-merge",
    "gh pr merge",
    "stripe",
    "payment link",
]

REQUIRED_GOVERNANCE_FILES = [
    "tools/hgfm_doc_ci.py",
    "tools/revenue_evidence_ci.py",
    "tools/knowledge_respect_ci.py",
    "docs/hgfm/HGFM_DOCUMENTATION_INDEX.md",
    "docs/hgfm/HGFM_DOCUMENTATION_PROJECTORS.md",
    "docs/ethics/KNOWLEDGE_RESPECT_PROTOCOL.md",
    "docs/ethics/knowledge_respect.schema.json",
    "docs/ethics/CULTURAL_CLAIMS_REGISTER.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/REVENUE_EVIDENCEGATE_V0_9.md",
    "products/tfuga-hyper-revenue-reactor-v0.8/CHECKOUT_T4_EVIDENCE_PROTOCOL.md",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def run_script(script: str) -> None:
    print(f"[RUN] {script}")
    result = subprocess.run([sys.executable, script], cwd=ROOT, text=True)
    if result.returncode != 0:
        fail(f"script failed: {script}")
    ok(f"script passed: {script}")


def check_required_files() -> None:
    for rel in REQUIRED_GOVERNANCE_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required governance file: {rel}")
        ok(f"required file exists: {rel}")


def check_workflows_are_read_only() -> None:
    for rel in WORKFLOWS:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing workflow: {rel}")
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_WORKFLOW_TOKENS:
            if token in text:
                fail(f"forbidden workflow token in {rel}: {token}")
        if "contents: read" not in text:
            fail(f"workflow should use contents: read: {rel}")
        ok(f"workflow is read-only gated: {rel}")


def check_release_candidate_docs() -> None:
    rc = ROOT / "products" / "tfuga-hyper-revenue-reactor-v0.8" / "PUBLIC_RELEASE_CANDIDATE_CHECKLIST.md"
    if rc.exists():
        text = rc.read_text(encoding="utf-8").lower()
        for token in ["support", "privacy", "refund", "checkout", "t4", "human review"]:
            if token not in text:
                fail(f"release candidate checklist missing token: {token}")
        ok("release candidate checklist tokens")
    else:
        print("[WARN] release candidate checklist not present yet")


def check_knowledge_respect_docs() -> None:
    protocol = ROOT / "docs" / "ethics" / "KNOWLEDGE_RESPECT_PROTOCOL.md"
    text = protocol.read_text(encoding="utf-8").lower()
    for token in ["useallowed", "benefit", "attribution", "review", "k0", "k6"]:
        if token not in text:
            fail(f"knowledge respect protocol missing token: {token}")
    ok("knowledge respect protocol tokens")


def main() -> int:
    print("[TFUGA-UNIFIED-GOVERNANCE] Starting checks")
    check_required_files()
    check_workflows_are_read_only()
    run_script("tools/hgfm_doc_ci.py")
    run_script("tools/revenue_evidence_ci.py")
    run_script("tools/knowledge_respect_ci.py")
    check_release_candidate_docs()
    check_knowledge_respect_docs()
    print("[TFUGA-UNIFIED-GOVERNANCE] All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
