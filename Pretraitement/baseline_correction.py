"""
baseline_correction.py — Raman AI Preprocessing Module (Optech)
---------------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Correct baseline fluorescence and background drift in Raman spectra.

Implemented methods:
1. ALS (Asymmetric Least Squares)
2. AirPLS (Adaptive Iteratively Reweighted Penalized Least Squares)
3. SNIP (Statistical-sensitive Non-linear Iterative Peak-clipping)

Dependencies:
    numpy, scipy.sparse, scipy.sparse.linalg
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# -------------------------------------------------------------------------
# 🔹 1. Asymmetric Least Squares (ALS)
# -------------------------------------------------------------------------
def baseline_als(y, lam=1e6, p=0.001, niter=10):
    """
    Asymmetric Least Squares baseline correction.

    Parameters
    ----------
    y : np.ndarray
        Intensity vector.
    lam : float
        Smoothness parameter (higher = smoother baseline).
    p : float
        Asymmetry parameter (0 < p < 1).
    niter : int
        Number of iterations.

    Returns
    -------
    baseline : np.ndarray
    """
    L = len(y)
    D = sp.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    D = D.dot(D.T)
    w = np.ones(L)
    for i in range(niter):
        W = sp.spdiags(w, 0, L, L)
        Z = W + lam * D
        z = spla.spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


# -------------------------------------------------------------------------
# 🔹 2. AirPLS (Adaptive Iteratively Reweighted Penalized LS)
# -------------------------------------------------------------------------
def baseline_airpls(y, lam=1e6, niter=15):
    """
    Adaptive baseline correction using AirPLS algorithm.
    Reference: Zhang et al., Analytica Chimica Acta 2005.

    Returns
    -------
    baseline : np.ndarray
    """
    L = len(y)
    D = sp.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    D = D.dot(D.T)
    w = np.ones(L)
    for i in range(niter):
        W = sp.spdiags(w, 0, L, L)
        Z = W + lam * D
        z = spla.spsolve(Z, w * y)
        d = y - z
        dn = d[d < 0]
        m = np.mean(np.abs(dn))
        s = np.std(dn)
        w = np.exp(- (d / (2 * (s + 1e-6)))**2)
        w[y < z] = 0.0
        if np.mean(np.abs(d)) < 0.001 * np.max(y):
            break
    return z


# -------------------------------------------------------------------------
# 🔹 3. SNIP Baseline (Optional)
# -------------------------------------------------------------------------
def baseline_snip(y, niter=24):
    """
    SNIP algorithm: iteratively smooths the logarithm of intensity.

    Returns
    -------
    baseline : np.ndarray
    """
    y_log = np.log1p(np.maximum(y, 0))
    b = y_log.copy()
    for i in range(niter):
        b[i+1:-i-1] = np.minimum(b[i+1:-i-1],
                                 0.5 * (b[i:-i-2] + b[i+2:-i]))
    return np.expm1(b)


# -------------------------------------------------------------------------
# 🔹 4. BaselineCorrector Class
# -------------------------------------------------------------------------
class BaselineCorrector:
    """
    Unified baseline correction module for Raman AI preprocessing.
    """

    def __init__(self, method="als", lam=1e6, p=0.001, niter=10):
        """
        Parameters
        ----------
        method : str
            'als', 'airpls', or 'snip'.
        lam : float
            Smoothness parameter (for ALS/AirPLS).
        p : float
            Asymmetry (for ALS).
        niter : int
            Number of iterations.
        """
        self.method = method.lower()
        self.lam = lam
        self.p = p
        self.niter = niter

    # -----------------------------------------------------

    def apply(self, x, y):
        """
        Apply baseline correction to a spectrum.

        Parameters
        ----------
        x : np.ndarray
            Raman shift (cm⁻¹)
        y : np.ndarray
            Intensities (arbitrary units)

        Returns
        -------
        (x, y_corrected, baseline)
        """
        if self.method == "als":
            baseline = baseline_als(y, self.lam, self.p, self.niter)
        elif self.method == "airpls":
            baseline = baseline_airpls(y, self.lam, self.niter)
        elif self.method == "snip":
            baseline = baseline_snip(y, self.niter)
        else:
            raise ValueError(f"Unknown baseline method: {self.method}")

        y_corr = y - baseline
        return x, y_corr, baseline
