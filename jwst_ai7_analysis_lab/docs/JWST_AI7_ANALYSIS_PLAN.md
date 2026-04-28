# JWST AI-7 Analysis Plan

## Goal

Create reproducible, conservative, claim-level analysis for public or authorized JWST data.

## Pipeline

```text
MAST -> manifest -> calibration ledger -> quality gates -> image/spectral/cube analysis -> conservative multiscale candidates -> DCT claim packet -> reproducible report
```

## Product stages

- Stage 0: raw uncalibrated products, typically `uncal.fits`.
- Stage 1: detector-corrected count-rate products, typically `rate.fits` or `rateints.fits`.
- Stage 2: calibrated individual products, typically `cal.fits` or `calints.fits`.
- Stage 3: combined science products, typically `i2d.fits`, `s3d.fits`, or `x1d.fits`.

## Required metadata

Every claim should preserve:

```text
program_id, target_name, instrument, detector/filter/grating, product stage, CAL_VER, CRDS_CTX, filename, provenance URL
```

## Equations

```text
z = (lambda_obs - lambda_rest) / lambda_rest
SNR_line = sum(F_lambda - F_cont) / sqrt(sum(sigma_lambda^2))
EW = integral(1 - F_lambda/F_cont) d lambda
I_obs = PSF * I_sky + B + N
```

## AI-7 gates

```text
SourceOK + CalibrationVersionOK + QualityOK + PSFNoiseOK + UncertaintyOK + AlternativeTestOK + DCTReady + HumanReviewOK
```

## Conservative FFWT / multiscale rule

Multiscale or FFWT-like processing may propose candidate structures. It cannot prove them by itself. Proof must be checked on original calibrated products with PSF/noise alternatives and uncertainty accounting.

## First target suggestions

- SMACS 0723 or JADES / deep fields.
- CEERS / high-redshift galaxies.
- WASP-39b / exoplanet atmosphere spectra.
- NGC 3324 / star formation and dust.
- MIRI MRS cube targets / line maps.
