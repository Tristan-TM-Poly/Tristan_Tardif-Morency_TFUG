# AI-7 QC-CA Top 64^5 DCT Tensor

This extension lifts the Québec-Canada Institutional HyperAtlas from `64^4` to `64^5` by adding a fifth axis:

```text
E = DCT / proof / prototype / maturity gates
```

Total candidate hyperedges:

```text
64^5 = 1,073,741,824
```

Canonical equation:

```text
Opportunity5(a,b,c,d,e) = InstitutionSource[a] ⊗ Challenge[b] ⊗ Capability[c] ⊗ Action[d] ⊗ DCTGate[e]
```

This is a dependent extension of PR #14. It reuses the existing `top_64x64x64x64` axes and adds only the fifth axis plus a streaming generator.

## Files

- `axes/top_64_e_dct_axis.json`
- `generator/generate_top64x5_tensor.py`
- `examples/top64x5_seed_candidates.json`
- `reports/top64x5_report.md`

## Governance

Do not materialize all 1.07B candidates by default. Stream-score and keep only top-k candidates that pass:

```text
PrivacyOK + LicenseOK + HumanReviewOK + DCTReady
```
