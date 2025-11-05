"""
qc_report.py — Raman AI Preprocessing Module (Optech)
-----------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Evaluate Raman spectra quality and generate QC report (.xlsx + .pdf)

Checks performed:
1. Signal-to-Noise Ratio (SNR)
2. RMS baseline residual
3. Peak matching vs. reference
4. Area conservation
5. Outlier detection (Z-score)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pathlib import Path


# -------------------------------------------------------------------------
# 🔹 1. Fonctions de base
# -------------------------------------------------------------------------
def compute_snr(y):
    """
    Compute Signal-to-Noise Ratio (SNR).
    """
    signal = np.max(y) - np.min(y)
    noise = np.std(y[:50])  # bruit sur zone stable (ex. : 1ʳᵉ région)
    return 20 * np.log10(signal / (noise + 1e-12))


def baseline_rms(y_corr, y_ref=None):
    """
    Compute RMS deviation of baseline or corrected signal.
    """
    if y_ref is None:
        y_ref = np.zeros_like(y_corr)
    return np.sqrt(np.mean((y_corr - y_ref)**2))


def match_reference_peaks(x, y, ref_peaks, tol=2.0):
    """
    Compare measured peaks to known reference positions.
    Returns matching ratio (% of matched peaks).
    """
    peaks, _ = find_peaks(y, height=np.max(y)*0.1, distance=10)
    found = x[peaks]
    matches = sum(any(abs(f - r) <= tol for f in found) for r in ref_peaks)
    return (matches / len(ref_peaks)) * 100 if ref_peaks else np.nan


def zscore_outlier(y):
    """
    Detect global intensity outliers via z-score.
    """
    z = (y - np.mean(y)) / (np.std(y) + 1e-12)
    outlier_ratio = np.sum(np.abs(z) > 3) / len(z)
    return 100 * outlier_ratio


# -------------------------------------------------------------------------
# 🔹 2. Classe QCReporter
# -------------------------------------------------------------------------
class QCReporter:
    """
    Automated QC evaluator for Raman preprocessing pipeline.
    """

    def __init__(self, ref_peaks=[520.7], out_dir="qc_reports"):
        self.ref_peaks = ref_peaks
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(exist_ok=True)

    def evaluate(self, x, y_raw, y_corr):
        """
        Evaluate spectrum quality and produce report.

        Parameters
        ----------
        x : np.ndarray
            Raman shift axis (cm⁻¹)
        y_raw : np.ndarray
            Raw intensity
        y_corr : np.ndarray
            Preprocessed intensity (baseline-corrected)

        Returns
        -------
        qc_metrics : dict
        """
        snr = compute_snr(y_corr)
        rms = baseline_rms(y_corr)
        peak_match = match_reference_peaks(x, y_corr, self.ref_peaks)
        outlier_pct = zscore_outlier(y_corr)
        area_diff = abs(np.trapz(y_corr) - np.trapz(y_raw)) / (np.trapz(y_raw) + 1e-12) * 100

        qc_metrics = {
            "SNR (dB)": snr,
            "RMS baseline": rms,
            "Peak match (%)": peak_match,
            "Outliers (%)": outlier_pct,
            "Area diff (%)": area_diff,
        }

        return qc_metrics

    # --------------------------------------------------------------
    def generate_report(self, sample_id, x, y_raw, y_corr, qc_metrics):
        """
        Generate graphical + Excel report for a given sample.
        """
        # 📊 Figure PDF
        plt.figure(figsize=(8, 5))
        plt.plot(x, y_raw, label="Brut", alpha=0.5)
        plt.plot(x, y_corr, label="Prétraité", linewidth=1.8)
        plt.xlabel("Raman shift (cm⁻¹)")
        plt.ylabel("Intensité (a.u.)")
        plt.title(f"Spectre Raman — QC ({sample_id})")
        plt.legend()
        pdf_path = self.out_dir / f"{sample_id}_QC.pdf"
        plt.tight_layout()
        plt.savefig(pdf_path)
        plt.close()

        # 📘 Tableau Excel
        df = pd.DataFrame([qc_metrics])
        xlsx_path = self.out_dir / f"{sample_id}_QC.xlsx"
        df.to_excel(xlsx_path, index=False)

        return str(pdf_path), str(xlsx_path)
