# AI-7 QC-CA Top 64^8 MetaCanon Tensor

This extension lifts the Québec-Canada Institutional HyperAtlas from `64^6` to `64^8` by adding two axes:

```text
G = scale / territory / time / partner context
H = meta-canon / learning / transfer / reproduction
```

Total candidate hyperedges:

```text
64^8 = 281,474,976,710,656
```

Canonical equation:

```text
Opportunity8(a,b,c,d,e,f,g,h) = InstitutionSource[a] ⊗ Challenge[b] ⊗ Capability[c] ⊗ Action[d] ⊗ DCTGate[e] ⊗ ImpactOps[f] ⊗ ScaleContext[g] ⊗ MetaCanon[h]
```

## Why the seventh and eighth axes matter

`64^4` finds opportunity.

`64^5` demands proof.

`64^6` demands measured, reversible impact.

`64^7` adds scale, territory, time and stakeholder context.

`64^8` adds meta-learning, transfer, reproduction and canon governance.

## Safety rule

Never materialize `64^8`. This PR uses bounded beam search rather than exhaustive enumeration.

```text
generate massively in latent space, search sparsely, validate locally, canonize rarely
```

## Promotion rule

```text
Promote(edge8) = 1 iff Score > theta and PrivacyOK and LicenseOK and HumanReviewOK and DCTReady and ImpactMeasured and RollbackReady and ScaleReady and TransferReady
```

## Files

- `axes/top_64_g_scale_context_axis.json`
- `axes/top_64_h_metacanon_axis.json`
- `generator/generate_top64x8_beam.py`
- `reports/top64x8_metacanon_report.md`
- `examples/top64x8_seed_candidates.json`
- `tests/validate_top64x8_beam.py`
