"""
noise_filter.py — Raman AI Preprocessing Module (Optech)
--------------------------------------------------------
Author: Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Clean Raman spectra from cosmic spikes and high-frequency noise.

Techniques implemented:
1. Cosmic spike removal (median-based outlier detection)
2. Savitzky–Golay smoothing filter
3. Optional wavelet denoising (Daubechies family)

Dependencies:
    numpy, scipy.signal, pywt (optional)
"""

import numpy as np
from scipy.signal import savgol_filter
import PyWavelets as pywt


class NoiseFilter:
    """
    Clean Raman spectrum using spike removal and denoising filters.
    """

    def __init__(self,
                 spike_sigma=5.0,
                 spike_window=3,
                 sg_window=15,
                 sg_polyorder=3,
                 wavelet=None,
                 wavelet_level=2):
        """
        Initialize noise filtering parameters.

        Parameters
        ----------
        spike_sigma : float
            Threshold (in standard deviations) for spike detection.
        spike_window : int
            Number of neighbors used for local median replacement.
        sg_window : int
            Window length for Savitzky–Golay smoothing (must be odd).
        sg_polyorder : int
            Polynomial order for Savitzky–Golay smoothing.
        wavelet : str or None
            Name of the wavelet for denoising (e.g., 'db4'). If None, skip.
        wavelet_level : int
            Decomposition level for wavelet denoising.
        """
        self.spike_sigma = spike_sigma
        self.spike_window = spike_window
        self.sg_window = sg_window
        self.sg_polyorder = sg_polyorder
        self.wavelet = wavelet
        self.wavelet_level = wavelet_level

    # -----------------------------------------------------

    def _remove_cosmic_spikes(self, y):
        """
        Detect and remove cosmic spikes using median-based replacement.

        Returns
        -------
        np.ndarray : cleaned intensity vector
        """
        y_clean = y.copy()
        residual = y - savgol_filter(y, 7, 2)
        threshold = self.spike_sigma * np.std(residual)

        for i in range(1, len(y) - 1):
            if abs(residual[i]) > threshold:
                local_start = max(0, i - self.spike_window)
                local_end = min(len(y), i + self.spike_window)
                y_clean[i] = np.median(y[local_start:local_end])
        return y_clean

    # -----------------------------------------------------

    def _apply_wavelet_denoise(self, y):
        """
        Apply wavelet denoising to reduce high-frequency noise.
        """
        coeffs = pywt.wavedec(y, self.wavelet, level=self.wavelet_level)
        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        uthresh = sigma * np.sqrt(2 * np.log(len(y)))
        coeffs_thresh = [pywt.threshold(c, value=uthresh, mode='soft') for c in coeffs]
        return pywt.waverec(coeffs_thresh, self.wavelet)

    # -----------------------------------------------------

    def apply(self, x, y):
        """
        Full cleaning pipeline:
        1. Remove cosmic spikes.
        2. Apply Savitzky–Golay smoothing.
        3. Optionally apply wavelet denoising.

        Parameters
        ----------
        x : np.ndarray
            Raman shift axis (cm⁻¹)
        y : np.ndarray
            Raw intensity values

        Returns
        -------
        (x, y_clean) : tuple of np.ndarray
        """
        # Step 1: Spike cleaning
        y_clean = self._remove_cosmic_spikes(y)

        # Step 2: Savitzky–Golay smoothing
        y_smooth = savgol_filter(y_clean, self.sg_window, self.sg_polyorder)

        # Step 3: Optional wavelet denoising
        if self.wavelet is not None:
            y_final = self._apply_wavelet_denoise(y_smooth)
        else:
            y_final = y_smooth

        return x, y_final
    

