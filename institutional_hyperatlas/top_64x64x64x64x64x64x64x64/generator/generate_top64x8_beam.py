#!/usr/bin/env python3
"""Bounded beam search for the AI-7 QC-CA Top 64^8 MetaCanon tensor.

This generator never materializes 64^8. It builds candidate paths incrementally
and keeps only a fixed beam width after each axis expansion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def stable_hash_score(items):
    h = hashlib.sha256("|".join(items).encode("utf-8")).hexdigest()
    return int(h[:8], 16) / 0xffffffff


def kw_score(text, kws):
    t = text.lower()
    return sum(1 for k in kws if k in t) / max(1, len(kws))


KWS = {
    "impact": ["energy", "water", "climate", "materials", "ai", "municipal", "grid", "space", "measured", "impact"],
    "governance": ["privacy", "license", "review", "audit", "rollback", "human", "schema", "ci", "safety"],
    "proof": ["dct", "test", "proof", "reproduced", "benchmark", "uncertainty", "counterexample"],
    "transfer": ["transfer", "template", "registry", "canon", "reusable", "education", "paper", "grant"],
    "risk": ["outreach", "personal", "production", "high risk", "blocked", "permission", "security"]
}


def score_path(path):
    text = " ".join(path)
    positive = (
        0.24 * kw_score(text, KWS["impact"])
        + 0.24 * kw_score(text, KWS["governance"])
        + 0.24 * kw_score(text, KWS["proof"])
        + 0.18 * kw_score(text, KWS["transfer"])
        + 0.10 * stable_hash_score(path)
    )
    risk = 0.22 * kw_score(text, KWS["risk"])
    return round(max(0.0, min(1.0, positive - risk)), 6)


def top_beam(paths, width):
    scored = [(score_path(path), path) for path in paths]
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [path for _, path in scored[:width]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--axes4", default="institutional_hyperatlas/top_64x64x64x64/axes/top_64_axes.json")
    parser.add_argument("--axis5", default="institutional_hyperatlas/top_64x64x64x64x64/axes/top_64_e_dct_axis.json")
    parser.add_argument("--axis6", default="institutional_hyperatlas/top_64x64x64x64x64x64/axes/top_64_f_impactops_axis.json")
    parser.add_argument("--axis7", default="institutional_hyperatlas/top_64x64x64x64x64x64x64x64/axes/top_64_g_scale_context_axis.json")
    parser.add_argument("--axis8", default="institutional_hyperatlas/top_64x64x64x64x64x64x64x64/axes/top_64_h_metacanon_axis.json")
    parser.add_argument("--beam-width", type=int, default=256)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--out", default="institutional_hyperatlas/top_64x64x64x64x64x64x64x64/reports/generated_top64x8_beam.json")
    args = parser.parse_args()

    axes4 = json.loads(Path(args.axes4).read_text(encoding="utf-8"))
    axis5 = json.loads(Path(args.axis5).read_text(encoding="utf-8"))
    axis6 = json.loads(Path(args.axis6).read_text(encoding="utf-8"))
    axis7 = json.loads(Path(args.axis7).read_text(encoding="utf-8"))
    axis8 = json.loads(Path(args.axis8).read_text(encoding="utf-8"))

    axes = [
        axes4["A_institutions_sources"],
        axes4["B_challenges_sectors"],
        axes4["C_ai7_capabilities"],
        axes4["D_actions_governance"],
        axis5["E_dct_proof_prototype_maturity_gates"],
        axis6["F_impactops_field_feedback_rollback_adoption"],
        axis7["G_scale_territory_time_partner_context"],
        axis8["H_metacanon_learning_transfer_reproduction"],
    ]

    beam = [[]]
    for axis in axes:
        expanded = [path + [value] for path in beam for value in axis]
        beam = top_beam(expanded, args.beam_width)

    rows = []
    for rank, path in enumerate(top_beam(beam, args.limit), start=1):
        rows.append({
            "rank": rank,
            "score": score_path(path),
            "institution_source": path[0],
            "challenge_sector": path[1],
            "ai7_capability": path[2],
            "action": path[3],
            "dct_gate": path[4],
            "impactops_gate": path[5],
            "scale_context": path[6],
            "metacanon_gate": path[7],
        })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
