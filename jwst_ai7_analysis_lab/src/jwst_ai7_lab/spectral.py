#!/usr/bin/env python3
"""JWST AI-7 spectral utilities.

These functions are small, dependency-free, and intended for reproducible tests.
They do not replace instrument-specific JWST calibration or expert analysis.
"""
from __future__ import annotations

import math

C_KMS = 299_792.458


def compute_redshift(lambda_obs: float, lambda_rest: float) -> float:
    """Compute z = (lambda_obs - lambda_rest) / lambda_rest."""
    if lambda_rest <= 0:
        raise ValueError("lambda_rest must be positive")
    return (lambda_obs - lambda_rest) / lambda_rest


def velocity_offset(lambda_obs: float, lambda_ref_obs: float) -> float:
    """Return velocity offset in km/s around an observed reference wavelength."""
    if lambda_ref_obs <= 0:
        raise ValueError("lambda_ref_obs must be positive")
    return C_KMS * (lambda_obs - lambda_ref_obs) / lambda_ref_obs


def line_snr(flux, continuum, sigma) -> float:
    """Integrated line SNR = sum(F - C) / sqrt(sum(sigma^2))."""
    flux = list(map(float, flux))
    continuum = list(map(float, continuum))
    sigma = list(map(float, sigma))
    if not (len(flux) == len(continuum) == len(sigma)):
        raise ValueError("flux, continuum, and sigma must have the same length")
    denom = math.sqrt(sum(s * s for s in sigma))
    if denom == 0:
        raise ValueError("sigma norm must be non-zero")
    return sum(f - c for f, c in zip(flux, continuum)) / denom


def equivalent_width(wavelength, flux, continuum) -> float:
    """Equivalent width integral int(1 - F/Fc) dlambda by trapezoids.

    Positive values follow the absorption convention. For emission-line convention,
    use -EW.
    """
    wavelength = list(map(float, wavelength))
    flux = list(map(float, flux))
    continuum = list(map(float, continuum))
    if not (len(wavelength) == len(flux) == len(continuum)):
        raise ValueError("wavelength, flux, continuum must have the same length")
    if len(wavelength) < 2:
        raise ValueError("at least two wavelength points are required")
    if any(c == 0 for c in continuum):
        raise ValueError("continuum must be non-zero")
    y = [1.0 - f / c for f, c in zip(flux, continuum)]
    return sum(0.5 * (y[i] + y[i + 1]) * (wavelength[i + 1] - wavelength[i]) for i in range(len(wavelength) - 1))
