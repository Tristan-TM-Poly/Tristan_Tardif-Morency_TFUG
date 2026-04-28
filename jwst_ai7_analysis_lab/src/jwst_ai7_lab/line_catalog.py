#!/usr/bin/env python3
"""Small reusable astrophysical line catalog for JWST AI-7 analysis.

Wavelengths are approximate vacuum/rest wavelengths in micrometers unless noted.
This lightweight catalog is for candidate matching and tests, not final publication.
"""
from __future__ import annotations

COMMON_LINES_UM = {
    "Lyman_alpha": 0.121567,
    "H_beta": 0.486133,
    "OIII_4959": 0.495891,
    "OIII_5007": 0.500684,
    "H_alpha": 0.656281,
    "NII_6583": 0.658345,
    "SII_6716": 0.671647,
    "SII_6731": 0.673085,
    "Pa_beta": 1.2818,
    "Pa_alpha": 1.8751,
    "Br_gamma": 2.1661,
    "PAH_3p3": 3.3,
    "PAH_6p2": 6.2,
    "PAH_7p7": 7.7,
    "PAH_11p3": 11.3,
}


def observed_wavelength(rest_um: float, z: float) -> float:
    if rest_um <= 0:
        raise ValueError("rest_um must be positive")
    if z < -1:
        raise ValueError("z must be greater than -1")
    return rest_um * (1.0 + z)


def candidate_line_matches(lambda_obs_um: float, z_min: float = 0.0, z_max: float = 20.0, tolerance_um: float = 0.01):
    """Return catalog lines whose implied redshift is in range.

    tolerance_um is retained for API symmetry and future matching against an expected redshift;
    this function currently reports all physically plausible redshifts in range.
    """
    if lambda_obs_um <= 0:
        raise ValueError("lambda_obs_um must be positive")
    matches = []
    for name, rest in COMMON_LINES_UM.items():
        z = lambda_obs_um / rest - 1.0
        if z_min <= z <= z_max:
            matches.append({"line": name, "rest_um": rest, "z": round(z, 6), "lambda_obs_um": lambda_obs_um})
    return sorted(matches, key=lambda item: item["z"])
