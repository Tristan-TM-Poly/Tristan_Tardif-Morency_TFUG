"""
raman_tfu_thermo.py — TFU–Thermodynamic Raman Spectrum Generator
-----------------------------------------------------------------
Couples temperature and fractal dimension (Df(T)) to Raman analytical model.
"""

import numpy as np
import matplotlib.pyplot as plt
from raman_analytic import raman_analytic

def Df_TFU(T, T0=300, Tc=1500, eta=0.08):
    """Fractal dimension as a function of temperature."""
    return 1.0 + eta * np.log(1.0 + (T - T0) / Tc)

def update_modes_T(T, modes, T0=300):
    """Return temperature-adjusted Raman mode parameters."""
    updated = []
    for m in modes:
        A0, nu0, sigma0 = m["A"], m["nu"], m["sigma"]
        alpha = m.get("alpha", 1e-5)
        beta = m.get("beta", 5e-4)
        gamma = m.get("gammaT", 2e-3)
        nu_T = nu0 * (1 - alpha * (T - T0))
        sigma_T = sigma0 * (1 + beta * (T - T0))
        A_T = A0 * np.exp(-gamma * (T - T0))
        mT = m.copy()
        mT.update({"A": A_T, "nu": nu_T, "sigma": sigma_T})
        updated.append(mT)
    return updated

def raman_tfu_thermo(nu, modes, T, T0=300, Tc=1500, eta=0.08, lam=1.0):
    """Compute TFU–thermodynamic Raman spectrum."""
    Df = Df_TFU(T, T0, Tc, eta)
    modes_T = update_modes_T(T, modes, T0)
    return raman_analytic(nu, modes_T, Df=Df, lam=lam, T=T), Df
