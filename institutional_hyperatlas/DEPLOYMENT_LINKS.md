# AI-7 QC-CA HyperAtlas Deployment Links

This file indexes the reviewable deployment surfaces for the AI-7 Québec-Canada Institutional HyperAtlas.

## Canonical seed

- Main PR: https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG/pull/14
- Module path: `institutional_hyperatlas/top_64x64x64x64/`
- Tensor size: `64^4 = 16,777,216` candidate opportunity hyperedges.

## Propagation issues

- TFUGA-AI7-TRISTAN2: https://github.com/Tristan-TM-Poly/TFUGA-AI7-TRISTAN2/issues/1
- TTM-TFUGA-AI7-TRISTAN2: https://github.com/Tristan-TM-Poly/TTM-TFUGA-AI7-TRISTAN2/issues/1
- PEFA-FractalEnergySystem: https://github.com/Tristan-TM-Poly/PEFA-FractalEnergySystem/issues/1
- TFUGAG mirror: https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUGAG/issues/1
- TFACC audit: https://github.com/Tristan-TM-Poly/TFACC/issues/1
- Web and game surface: https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG/issues/15

## Promotion rule

`Promote(edge) = 1 iff Score > theta and PrivacyOK and LicenseOK and HumanReviewOK`.

## Gates

- Keep changes reviewable.
- Keep deployments manual until checks pass.
- Keep repository changes reversible.
- Keep public outputs institution-level unless reviewed.
- Keep PR #14 unmerged until mixed Vercel status is resolved or waived.

## Next best PR

`schema validation + privacy gate + license gate + CI test`.
