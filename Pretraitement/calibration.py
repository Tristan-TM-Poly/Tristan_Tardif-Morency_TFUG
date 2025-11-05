"""
calibration.py — Raman AI Preprocessing Module (Optech)
-------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Calibrate Raman spectra in wavenumber (cm⁻¹) and intensity.

Implements:
1. Wavenumber calibration using reference peaks (e.g., Si 520.7 cm⁻¹)
2. Intensity correction using instrument response curve

Dependencies:
    numpy, scipy.signal, json
"""

import numpy as np
import json
from scipy.signal import find_peaks
from scipy.interpolate import interp1d


# -------------------------------------------------------------------------
# 🔹 1. Peak-based Wavenumber Calibration
# -------------------------------------------------------------------------
def calibrate_wavenumber(x_raw, y_raw, ref_peaks, measured_peaks, order=1):
    """
    Align the measured Raman axis to reference standards.

    Parameters
    ----------
    x_raw : np.ndarray
        Raw Raman shift axis (cm⁻¹, uncalibrated)
    y_raw : np.ndarray
        Measured intensity
    ref_peaks : list[float]
        True reference peak positions (e.g., [520.7])
    measured_peaks : list[float]
        Detected peak positions on the raw data
    order : int
        Polynomial order for correction (1 = linear, 2 = quadratic)

    Returns
    -------
    x_cal : np.ndarray
        Calibrated Raman shift axis
    coeffs : np.ndarray
        Polynomial coefficients of calibration
    """
    coeffs = np.polyfit(measured_peaks, ref_peaks, order)
    poly = np.poly1d(coeffs)
    x_cal = poly(x_raw)
    return x_cal, coeffs


# -------------------------------------------------------------------------
# 🔹 2. Instrument Response Correction
# -------------------------------------------------------------------------
def correct_instrument_response(x, y, response_file="instrument_response.json"):
    """
    Apply intensity correction using measured instrument response.

    Parameters
    ----------
    x : np.ndarray
        Raman shift axis (cm⁻¹)
    y : np.ndarray
        Measured intensity
    response_file : str
        JSON file containing instrument response curve
        Example:
        {
          "x": [400, 600, 800, ...],
          "response": [1.0, 0.95, 0.90, ...]
        }

    Returns
    -------
    y_corr : np.ndarray
        Corrected intensity
    """
    try:
        with open(response_file, "r") as f:
            data = json.load(f)
        x_resp = np.array(data["x"])
        r = np.array(data["response"])
        interp = interp1d(x_resp, r, kind='linear', fill_value="extrapolate")
        response_interp = interp(x)
        y_corr = y / (response_interp + 1e-9)
        return y_corr
    except FileNotFoundError:
        print("[Warning] Instrument response file not found. Skipping correction.")
        return y


# -------------------------------------------------------------------------
# 🔹 3. Calibrator Class
# -------------------------------------------------------------------------
class Calibrator:
    """
    Raman wavenumber and intensity calibration module.
    """

    def __init__(self, ref_peaks=[520.7], response_file=None, order=1):
        self.ref_peaks = ref_peaks
        self.response_file = response_file
        self.order = order

    def detect_peaks(self, x, y, height_ratio=0.1):
        """
        Automatically detect main peaks in the measured spectrum.
        """
        height_thresh = np.max(y) * height_ratio
        peaks, _ = find_peaks(y, height=height_thresh, distance=20)
        return x[peaks]

    def apply(self, x, y):
        """
        Full calibration pipeline.

        Steps:
        1. Detect measured peaks
        2. Align to reference
        3. Apply instrument response correction

        Returns
        -------
        (x_cal, y_corr, coeffs)
        """
        measured_peaks = self.detect_peaks(x, y)
        n_ref = min(len(measured_peaks), len(self.ref_peaks))

        if n_ref == 0:
            print("[Warning] No peaks detected — skipping wavenumber calibration.")
            x_cal = x
            coeffs = None
        else:
            x_cal, coeffs = calibrate_wavenumber(
                x, y, self.ref_peaks[:n_ref], measured_peaks[:n_ref], self.order
            )

        # Apply instrument response correction
        y_corr = correct_instrument_response(x_cal, y, self.response_file) \
                 if self.response_file else y

        return x_cal, y_corr, coeffs
