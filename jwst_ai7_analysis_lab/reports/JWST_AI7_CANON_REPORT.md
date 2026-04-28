# JWST AI-7 Canon Report v0.1

## Canonical equation

```text
P_AI7_JWST = DCT o Gates o Physics o Calibration o MAST
```

## Spectral equations

```text
z = (lambda_obs - lambda_rest) / lambda_rest
SNR_line = sum(F_lambda - F_cont) / sqrt(sum(sigma_lambda^2))
EW = integral(1 - F_lambda/F_cont) d lambda
```

## Image model

```text
I_obs = PSF * I_sky + B + N
```

## Conservative multiscale rule

Wavelet, fractal, or FFWT-like filters can propose candidates, but proof must be performed on original calibrated products with uncertainty, PSF/noise checks, and an alternate test.

## DCT claim graph

```text
claim -> data products -> calibration -> equations -> code -> uncertainty -> tests -> limitations
```

## Promotion rule

```text
Promote(claim) = 1 iff DataOK and CalibrationOK and QualityOK and UncertaintyOK and DCTReady and HumanReviewOK
```

## Current status

This lab is a scaffold. It does not claim new discoveries by itself.
