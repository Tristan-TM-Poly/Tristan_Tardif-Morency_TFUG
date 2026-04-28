#!/usr/bin/env python3
"""Stream-score the AI-7 QC-CA Top 64^5 DCT tensor.

This generator depends on PR #14's 64^4 axes and adds the E axis from this folder.
It does not materialize 1.07B rows. It keeps only a top-k heap.
"""
import argparse
import hashlib
import heapq
import itertools
import json
from pathlib import Path


def stable_hash_score(items):
    h = hashlib.sha256("|".join(items).encode("utf-8")).hexdigest()
    return int(h[:8], 16) / 0xffffffff


def kw_score(text, kws):
    t = text.lower()
    return sum(1 for k in kws if k in t) / max(1, len(kws))


IMPACT_KWS = ["energy", "water", "climate", "materials", "opto", "raman", "ai", "municipal", "mining", "battery", "grid", "space", "privacy"]
AI7_KWS = ["hfmc", "ffwt", "hypergraph", "yggdrasil", "ai-7", "power score", "privacy", "license", "prototype", "canon", "tensor", "least-action"]
ACTION_KWS = ["verify", "review", "test", "pilot", "dct", "score", "privacy", "license", "prototype"]
DCT_KWS = ["dct", "test", "proof", "review", "passed", "ready", "prototype", "audit", "schema", "ci", "canon"]
RISK_KWS = ["outreach", "industry", "business", "health", "privacy", "download", "sync", "real", "personal", "production"]


def score_tuple(a, b, c, d, e):
    impact = (
        0.25 * kw_score(a + " " + b, IMPACT_KWS)
        + 0.20 * kw_score(c, AI7_KWS)
        + 0.20 * kw_score(d, ACTION_KWS)
        + 0.20 * kw_score(e, DCT_KWS)
        + 0.15 * stable_hash_score([a, b, c, d, e])
    )
    risk = 0.22 * kw_score(a + " " + b + " " + c + " " + d + " " + e, RISK_KWS)
    governance_bonus = 0.20 * kw_score(e + " " + d, ["privacy", "license", "review", "audit", "rollback", "human", "schema", "ci"])
    return round(max(0.0, min(1.0, impact + governance_bonus - risk)), 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axes4", default="institutional_hyperatlas/top_64x64x64x64/axes/top_64_axes.json")
    ap.add_argument("--axis5", default="institutional_hyperatlas/top_64x64x64x64x64/axes/top_64_e_dct_axis.json")
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--out", default="institutional_hyperatlas/top_64x64x64x64x64/reports/generated_top64x5.json")
    args = ap.parse_args()

    axes4 = json.loads(Path(args.axes4).read_text(encoding="utf-8"))
    axis5 = json.loads(Path(args.axis5).read_text(encoding="utf-8"))

    A = axes4["A_institutions_sources"]
    B = axes4["B_challenges_sectors"]
    C = axes4["C_ai7_capabilities"]
    D = axes4["D_actions_governance"]
    E = axis5["E_dct_proof_prototype_maturity_gates"]

    heap = []
    for a, b, c, d, e in itertools.product(A, B, C, D, E):
        sc = score_tuple(a, b, c, d, e)
        item = (sc, a, b, c, d, e)
        if len(heap) < args.limit:
            heapq.heappush(heap, item)
        elif sc > heap[0][0]:
            heapq.heapreplace(heap, item)

    rows = sorted(heap, reverse=True)
    out = [
        {
            "rank": i + 1,
            "score": sc,
            "institution_source": a,
            "challenge_sector": b,
            "ai7_capability": c,
            "action": d,
            "dct_gate": e,
        }
        for i, (sc, a, b, c, d, e) in enumerate(rows)
    ]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} rows to {out_path}")


if __name__ == "__main__":
    main()
