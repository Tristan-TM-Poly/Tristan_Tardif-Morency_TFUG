"""
derivative.py — Raman AI Preprocessing Module (Optech)
------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Compute first and second derivatives of Raman spectra with smoothing.

Implements:
1. Savitzky–Golay smoothing
2. First derivative
3. Second derivative

Dependencies:
    numpy, scipy.signal
"""

import numpy as np
from scipy.signal import savgol_filter


# -------------------------------------------------------------------------
# 🔹 1. Fonction principale de dérivation
# -------------------------------------------------------------------------
def derivative_spectrum(y, window=15, polyorder=3, deriv=1):
    """
    Compute Savitzky–Golay derivative of a Raman spectrum.

    Parameters
    ----------
    y : np.ndarray
        Raman intensity values.
    window : int
        Window length (odd, e.g., 11, 15, 21).
    polyorder : int
        Polynomial order for fitting (must be < window).
    deriv : int
        Derivative order (0 = smoothing, 1 = first, 2 = second).

    Returns
    -------
    y_deriv : np.ndarray
    """
    y = np.asarray(y)
    return savgol_filter(y, window_length=window, polyorder=polyorder, deriv=deriv)
    

# -------------------------------------------------------------------------
# 🔹 2. Classe orientée objet
# -------------------------------------------------------------------------
class Derivator:
    """
    Raman derivative and smoothing handler.
    """

    def __init__(self, window=15, polyorder=3, deriv=1):
        """
        Parameters
        ----------
        window : int
            Window length (odd number).
        polyorder : int
            Polynomial order.
        deriv : int
            Derivative order (1 = first, 2 = second).
        """
        self.window = window
        self.polyorder = polyorder
        self.deriv = deriv

    def apply(self, x, y):
        """
        Apply derivative smoothing to a Raman spectrum.

        Returns
        -------
        (x, y_deriv)
        """
        y_deriv = derivative_spectrum(y, self.window, self.polyorder, self.deriv)
        return x, y_deriv
