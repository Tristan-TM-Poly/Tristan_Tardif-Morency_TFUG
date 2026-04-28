# Top 64 x 64 x 64 x 64 AI-7 Québec-Canada Tensor

Generated: 2026-04-28

This package stores the four 64-element axes and a generator that can stream-score the full tensor.

Total combinations:

    64^4 = 16,777,216

Axes:
- A: institutions / sources
- B: challenges / sectors
- C: AI-7 capabilities
- D: governance actions

Compressed equation:

    Opportunity(a,b,c,d) = InstitutionSource[a] ⊗ Challenge[b] ⊗ Capability[c] ⊗ Action[d]

Promotion rule:

    Promote(a,b,c,d) = 1 iff Score > theta and PrivacyOK and LicenseOK and HumanReviewOK

Included output:
- examples/top_256_beam_candidates.json

To generate a top-k over the full tensor:

    python generator/generate_top_tensor.py --limit 1000 --out reports/generated_top_1000.json

Canonical interpretation:
The full 64^4 tensor is not meant to be read linearly. It is a generator of opportunity hyperedges.
AI-7 should materialize only the high-score, low-risk, reviewable edges.
