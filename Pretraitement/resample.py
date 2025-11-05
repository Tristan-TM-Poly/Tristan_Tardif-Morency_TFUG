"""
resample.py — Raman AI Preprocessing Module (Optech)
----------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Resample Raman spectra onto a uniform wavenumber grid.

Methods implemented:
1. Linear interpolation
2. Cubic-spline interpolation (optionnel)
3. Uniform step definition (Δν constant)

Dependencies:
    numpy, scipy.interpolate
"""

import numpy as np
from scipy.interpolate import interp1d


# -------------------------------------------------------------------------
# 🔹 Fonction principale
# -------------------------------------------------------------------------
def interp_spectrum(x, y, step=1.0, kind="linear"):
    """
    Interpolate a Raman spectrum onto a uniform axis.

    Parameters
    ----------
    x : np.ndarray
        Raman shift axis (cm⁻¹)
    y : np.ndarray
        Intensities
    step : float
        Desired spacing (Δν) in cm⁻¹
    kind : str
        Interpolation method ('linear', 'cubic', 'quadratic')

    Returns
    -------
    (x_new, y_new) : tuple of np.ndarray
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # 1️⃣ Crée un nouvel axe uniforme
    x_new = np.arange(np.min(x), np.max(x), step)

    # 2️⃣ Interpolation
    f = interp1d(x, y, kind=kind, fill_value="extrapolate")
    y_new = f(x_new)

    return x_new, y_new


# -------------------------------------------------------------------------
# 🔹 Classe orientée objet
# -------------------------------------------------------------------------
class Resampler:
    """
    Raman resampling/interpolation handler.
    """

    def __init__(self, step=1.0, kind="linear"):
        self.step = step
        self.kind = kind

    def apply(self, x, y):
        """
        Apply interpolation to obtain a uniform wavenumber grid.

        Returns
        -------
        (x_resampled, y_resampled)
        """
        return interp_spectrum(x, y, self.step, self.kind)
