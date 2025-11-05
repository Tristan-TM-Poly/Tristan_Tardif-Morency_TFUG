"""
normalize.py — Raman AI Preprocessing Module (Optech)
-----------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Normalize Raman intensities for AI and comparative analysis.

Implements:
1. Standard Normal Variate (SNV)
2. Min–Max Scaling
3. Area Normalization (unit area under curve)
"""

import numpy as np


# -------------------------------------------------------------------------
# 🔹 1. Standard Normal Variate (SNV)
# -------------------------------------------------------------------------
def snv(y):
    """
    Apply Standard Normal Variate normalization.
    y' = (y − mean(y)) / std(y)
    """
    y = np.asarray(y)
    return (y - np.mean(y)) / (np.std(y) + 1e-12)


# -------------------------------------------------------------------------
# 🔹 2. Min–Max Scaling
# -------------------------------------------------------------------------
def minmax(y, new_min=0.0, new_max=1.0):
    """
    Scale data to [new_min, new_max].
    """
    y = np.asarray(y)
    ymin, ymax = np.min(y), np.max(y)
    if ymax - ymin < 1e-12:
        return np.zeros_like(y)
    return new_min + (y - ymin) * (new_max - new_min) / (ymax - ymin)


# -------------------------------------------------------------------------
# 🔹 3. Area Normalization
# -------------------------------------------------------------------------
def area(y):
    """
    Divide by the area under the curve (∑ y).
    """
    y = np.asarray(y)
    A = np.trapz(y)
    return y / (A + 1e-12)


# -------------------------------------------------------------------------
# 🔹 4. Normalizer Class
# -------------------------------------------------------------------------
class Normalizer:
    """
    Unified interface for Raman normalization.
    """

    def __init__(self, method="snv"):
        self.method = method.lower()

    def apply(self, x, y):
        """
        Apply the chosen normalization.

        Parameters
        ----------
        x : np.ndarray
            Raman shift axis (cm⁻¹)
        y : np.ndarray
            Intensities (a.u.)

        Returns
        -------
        (x, y_norm)
        """
        if self.method == "snv":
            y_norm = snv(y)
        elif self.method == "minmax":
            y_norm = minmax(y)
        elif self.method == "area":
            y_norm = area(y)
        else:
            raise ValueError(f"Unknown normalization method '{self.method}'")
        return x, y_norm
