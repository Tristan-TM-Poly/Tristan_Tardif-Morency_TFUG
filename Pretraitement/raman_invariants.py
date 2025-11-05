"""
raman_invariants.py — Automatic extraction of TFU invariants from Raman spectra
-------------------------------------------------------------------------------
Author : Tristan Tardif-Morency
Purpose: Extract (ν, σ, A, Df) parameters from experimental or simulated spectra.
"""

import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from raman_tfu_thermo import Df_TFU

def gauss_lorentz_mix(nu, A, nu0, sigma, gamma, beta):
    gauss = np.exp(-((nu - nu0)**2) / (2*sigma**2))
    lorentz = gamma**2 / ((nu - nu0)**2 + gamma**2)
    return A * ((1 - beta)*gauss + beta*lorentz)

def extract_invariants(nu, I, T=300, T0=300, Tc=1500, eta=0.08, prominence=0.05):
    """
    Detect peaks, fit them, and extract Raman–TFU invariants.
    """
    peaks, props = find_peaks(I, prominence=np.max(I)*prominence)
    invariants = []

    for p in peaks:
        try:
            # Fenêtre locale autour du pic
            win = 40
            i_min, i_max = max(0, p-win), min(len(nu), p+win)
            x_fit = nu[i_min:i_max]
            y_fit = I[i_min:i_max]
            p0 = [np.max(y_fit), nu[p], 5.0, 3.0, 0.2]
            bounds = ([0, nu[p]-20, 0, 0, 0], [np.inf, nu[p]+20, 100, 20, 1])
            popt, pcov = curve_fit(gauss_lorentz_mix, x_fit, y_fit, p0=p0, bounds=bounds)
            A, nu0, sigma, gamma, beta = popt

            # Amplitude normalisée et facteur fractal apparent
            A_ref = A * np.exp((T - T0)/1000)  # amplitude attendue si Df=1
            Phi = A / A_ref
            Df_est = 1.0 + np.log(Phi + 1e-6) / 1.0  # approximation de e^{λ(Df−1)} ≈ Φ

            invariants.append({
                "nu": nu0,
                "sigma": sigma,
                "gamma": gamma,
                "beta": beta,
                "A": A,
                "Df_est": Df_est
            })
        except Exception:
            continue

    df = pd.DataFrame(invariants)
    df["T"] = T
    return df
