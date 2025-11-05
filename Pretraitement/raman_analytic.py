"""
raman_analytic.py — Analytical Raman Spectrum Generator (TFU / Optech)
----------------------------------------------------------------------
Author : Tristan Tardif-Morency
Purpose: Generate physically and fractally consistent Raman spectra.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, c, k

# Constantes physiques
hc = h * c * 100  # J·cm (conversion)

def phi_fractal(Df, lam=1.0, mode="exp"):
    if mode == "exp":
        return np.exp(lam * (Df - 1))
    elif mode == "poly":
        return 1 + (Df - 1)**2
    else:
        return 1.0


def raman_mode(nu, nu_k, A, sigma, gamma, beta, T):
    """One Raman mode (Gauss–Lorentz mix)."""
    gauss = np.exp(-((nu - nu_k)**2) / (2 * sigma**2))
    lorentz = gamma**2 / ((nu - nu_k)**2 + gamma**2)
    bose = 1 / (1 - np.exp(-hc * nu_k / (k * T)))
    return A * ((1 - beta) * gauss + beta * lorentz) * bose


def raman_analytic(nu, modes, Df=1.0, lam=1.0, T=300):
    """
    Generate analytic fractal Raman spectrum.

    Parameters
    ----------
    nu : np.ndarray
        Raman shift axis (cm⁻¹)
    modes : list of dict
        [{"A":..., "nu":..., "sigma":..., "gamma":..., "beta":...}, ...]
    Df : float
        Fractal dimension scaling factor
    lam : float
        Fractal amplification factor
    T : float
        Temperature (K)

    Returns
    -------
    I_f : np.ndarray
        Fractally scaled Raman intensity
    """
    total = np.zeros_like(nu)
    for m in modes:
        total += raman_mode(nu, m["nu"], m["A"], m["sigma"], m["gamma"], m["beta"], T)
    return phi_fractal(Df, lam) * total
