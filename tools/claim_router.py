#!/usr/bin/env python3
"""TFUGA Claim Router.

Classifies claims into evidence gates. This is a deterministic governance helper,
not a truth oracle. It does not promote, publish, deploy, spend, or merge.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

SCIENCE = ["prove", "validated", "physics", "raman", "spectrum", "material", "superconduct", "laboratory", "experiment", "simulation", "instrument"]
REVENUE = ["revenue", "passive income", "checkout", "stripe", "sponsor", "sale", "customer", "pricing", "buyer", "receipt"]
CULTURAL = ["first nations", "indigenous", "community knowledge", "elder", "knowledge keeper", "translation", "sacred", "ceremonial", "ocap", "care"]
DEPLOYMENT = ["merge", "deploy", "publish", "vercel", "github", "drive", "payment link", "upload", "public launch"]
PRODUCT = ["product", "delivery", "refund", "privacy", "support", "starter kit", "beta", "release candidate"]
SOFTWARE = ["code", "script", "test", "ci", "workflow", "package", "schema", "cli", "artifact"]

GATE_MAP = {
    "science": ("EvidenceGate / S4Gate", "S3", ["real data", "metadata", "controls", "calibration", "replicates", "uncertainty", "raw hashes"]),
    "software": ("CI + DCT++ + reproducibility notes", "S3", ["tests", "reproducible commands", "artifact hash", "failure modes"]),
    "revenue": ("RevenueEvidenceGate", "T3", ["payment mechanism", "receipt or sponsor log", "delivery evidence", "support contact", "privacy/refund review"]),
    "cultural": ("KnowledgeRespectGate", "K3", ["public source or permission", "attribution", "review path", "benefit-back", "no sensitive content"]),
    "product": ("ReleaseCandidateGate + RevenueEvidenceGate", "T3", ["delivery manifest", "support/refund/privacy", "checkout copy", "human review"]),
    "deployment": ("HumanReviewGate + OfficialActionGate", "T3", ["explicit approval", "rollback", "audit log", "external action evidence"]),
    "governance": ("UnifiedGovernanceCI", "S3/T3/K3", ["status line", "claims register", "CI gate", "human review path"]),
    "unknown": ("HumanReviewGate", "S2", ["claim classification", "source", "context", "required gate"]),
}

BLOCKED_BY_TYPE = {
    "science": ["physical validation without real data", "canon S6 without reproduction"],
    "revenue": ["guaranteed passive income", "autonomous revenue", "risk-free return"],
    "cultural": ["ownership or absorption of community knowledge", "AI replaces knowledge holders", "translate everything"],
    "deployment": ["auto-merge", "auto-deploy", "external mutation without review"],
    "product": ["buyer receives unspecified deliverables", "privacy/refund/support missing"],
    "software": ["untested package", "hidden side effects"],
    "governance": ["promoting claims only because docs exist"],
    "unknown": ["untyped claim promoted directly"],
}

@dataclass
class ClaimRoute:
    claim_id: str
    claim_text: str
    claim_type: str
    required_gate: str
    max_status_without_external_evidence: str
    missing_evidence: list[str]
    blocked_claims: list[str]
    next_least_action: str
    human_review_required: bool = True
    risk_level: str = "R2"


def count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def classify(text: str) -> str:
    t = text.lower()
    scores = {
        "science": count_hits(t, SCIENCE),
        "revenue": count_hits(t, REVENUE),
        "cultural": count_hits(t, CULTURAL),
        "deployment": count_hits(t, DEPLOYMENT),
        "product": count_hits(t, PRODUCT),
        "software": count_hits(t, SOFTWARE),
    }
    best, score = max(scores.items(), key=lambda kv: kv[1])
    if score == 0:
        return "unknown"
    if scores["deployment"] > 0 and any(x in t for x in ["merge", "deploy", "publish", "payment link", "stripe"]):
        return "deployment"
    if scores["cultural"] > 0:
        return "cultural"
    if scores["revenue"] > 0:
        return "revenue"
    return best


def route_claim(text: str, claim_id: str = "CLAIM-001") -> ClaimRoute:
    ctype = classify(text)
    gate, max_status, evidence = GATE_MAP[ctype]
    return ClaimRoute(
        claim_id=claim_id,
        claim_text=text,
        claim_type=ctype,
        required_gate=gate,
        max_status_without_external_evidence=max_status,
        missing_evidence=evidence,
        blocked_claims=BLOCKED_BY_TYPE[ctype],
        next_least_action=f"Route through {gate}; collect missing evidence before promotion.",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("claim", nargs="*", help="Claim text to route")
    parser.add_argument("--out", default="", help="Optional output JSON path")
    args = parser.parse_args()
    text = " ".join(args.claim).strip() or sys.stdin.read().strip()
    if not text:
        print("No claim text provided", file=sys.stderr)
        return 2
    packet = asdict(route_claim(text))
    payload = json.dumps(packet, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
