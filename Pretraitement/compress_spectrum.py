"""
compress_spectrum.py — Raman AI Physical Compression Module (Optech)
--------------------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Compress Raman spectra while preserving physical and fractal information.

Techniques implemented:
1. Peak-based compression (Lorentz/Gauss fitting)
2. Fractal transform (DFT / wavelet coefficients)
3. Adaptive quantization
4. Reconstruction function (inverse transform)
"""

import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import pywt
import json


# -------------------------------------------------------------------------
# 🔹 1. Fonctions utilitaires
# -------------------------------------------------------------------------
def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu)**2) / (2 * sigma**2))


def lorentzian(x, A, mu, gamma):
    return A * (gamma**2 / ((x - mu)**2 + gamma**2))


# -------------------------------------------------------------------------
# 🔹 2. Compression par ajustement de pics
# -------------------------------------------------------------------------
def fit_peaks(x, y, method="gaussian", prominence=0.05):
    """
    Fit main peaks with parametric models (Gaussian or Lorentzian).

    Returns
    -------
    params : list of dict
        Each dict contains (A, mu, sigma/gamma)
    """
    peaks, props = find_peaks(y, prominence=np.max(y) * prominence)
    model = gaussian if method == "gaussian" else lorentzian
    params = []

    for p in peaks:
        try:
            x_win = x[max(0, p - 20):min(len(x), p + 20)]
            y_win = y[max(0, p - 20):min(len(x), p + 20)]
            p0 = [np.max(y_win), x[p], 5.0]
            popt, _ = curve_fit(model, x_win, y_win, p0=p0)
            params.append({"A": popt[0], "mu": popt[1], "sigma": popt[2]})
        except Exception:
            continue

    return params


# -------------------------------------------------------------------------
# 🔹 3. Compression par ondelettes (Fractal transform)
# -------------------------------------------------------------------------
def fractal_wavelet_compress(y, wavelet="db4", level=4, threshold_ratio=0.05):
    """
    Apply discrete wavelet transform and truncate small coefficients.
    """
    coeffs = pywt.wavedec(y, wavelet, level=level)
    coeffs_flat = np.hstack(coeffs)
    thresh = threshold_ratio * np.max(np.abs(coeffs_flat))
    coeffs_thresh = [pywt.threshold(c, value=thresh, mode='soft') for c in coeffs]
    return coeffs_thresh


# -------------------------------------------------------------------------
# 🔹 4. Reconstruction du spectre compressé
# -------------------------------------------------------------------------
def reconstruct_wavelet(coeffs, wavelet="db4"):
    """
    Reconstruct compressed spectrum from truncated coefficients.
    """
    return pywt.waverec(coeffs, wavelet)


# -------------------------------------------------------------------------
# 🔹 5. Classe principale
# -------------------------------------------------------------------------
class SpectrumCompressor:
    """
    Compress Raman spectra using both peak fitting and wavelet transform.
    """

    def __init__(self, wavelet="db4", level=4, threshold_ratio=0.05, method="gaussian"):
        self.wavelet = wavelet
        self.level = level
        self.threshold_ratio = threshold_ratio
        self.method = method

    def compress(self, x, y):
        """
        Perform full physical compression.
        Returns a compressed dict representation.
        """
        params = fit_peaks(x, y, method=self.method)
        coeffs = fractal_wavelet_compress(y, self.wavelet, self.level, self.threshold_ratio)

        compression_dict = {
            "meta": {"wavelet": self.wavelet, "level": self.level, "method": self.method},
            "peaks": params,
            "coeffs": [c.tolist() for c in coeffs],
        }
        return compression_dict

    def decompress(self, compression_dict):
        """
        Reconstruct spectrum from compressed representation.
        """
        coeffs = [np.array(c) for c in compression_dict["coeffs"]]
        return reconstruct_wavelet(coeffs, compression_dict["meta"]["wavelet"])
