# JWST AI-7 Analysis Lab

Governed, reproducible scaffold for improved analysis of public or authorized James Webb Space Telescope data.

## Mission

Transform JWST products into claim-level DCT packets:

```text
MAST manifest -> calibration/version ledger -> quality gates -> image/spectral/cube analysis -> conservative multiscale candidates -> DCT claim packet -> reproducible report
```

## Scientific rule

A beautiful image is not proof. A detected structure must survive calibration/version checks, PSF/noise checks, uncertainty accounting, and at least one alternate-test path.

## Core gates

```text
SourceOK + CalibrationVersionOK + QualityOK + PSFNoiseOK + UncertaintyOK + AlternativeTestOK + DCTReady + HumanReviewOK
```

## Promotion rule

```text
Promote(claim) = 1 iff DataOK and CalibrationOK and QualityOK and UncertaintyOK and DCTReady and HumanReviewOK
```

## What this lab includes

- Manifest templates for JWST products.
- Spectral utilities: redshift, velocity offset, line SNR, equivalent width.
- Quality gate for conservative governance scoring.
- DCT claim packet builder.
- No-network smoke tests.
- Analysis plan and canon report.

## Safety

- No data download by default.
- No proprietary data access without authorization.
- No unverified scientific claims.
- No FFWT/multiscale enhancement as proof by itself.
- No cloud or workflow changes in this PR.

## Next target examples

- SMACS 0723 / deep field.
- CEERS or JADES / high-redshift galaxies.
- WASP-39b / exoplanet atmosphere spectra.
- NGC 3324 / star formation and dust.
- MIRI MRS cube targets / line maps.
