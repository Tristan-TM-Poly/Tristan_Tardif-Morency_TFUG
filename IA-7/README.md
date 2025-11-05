# TFU Superconductivity — Analytic Kernel

Minimal, deterministic TFU/TFUQ kernel to compute superconducting observables from a fractal parameter `Df` with power‑law renormalizations.

## Features
- Allen–Dynes/McMillan \(T_c\) with \( \lambda_{\mathrm{eff}}(D_f) \) and \( \Theta_{\mathrm{eff}}(D_f) \).
- \( \Delta_0, \xi_0, \lambda_L, \kappa, H_{c1}, H_{c2}, H_c, P_c \).
- \( J_d \) (depairing) and a simple pinning‑limited \( J_c \).
- Analytic inversion helper `estimate_Df_from_Tc()`.

## Usage (Python)
```python
from tfu_sc_analytic import SCInputs, compute_all, estimate_Df_from_Tc

p = SCInputs(theta0=900.0, lambda0=1.0, mu_star=0.12,
             vF0=2.0e5, mstar0=2.0*9.109e-31, ns0=8e27,
             Df_ref=1.2, al=0.70, at=0.70, ans=-0.70)

Df_star = estimate_Df_from_Tc(92.0, p)  # invert Tc -> Df
obs = compute_all(Df_star, p)
print(obs["Tc_K"], obs["lambdaL_nm"], obs["Hc2_T"])
```

## CLI Demo
```bash
python demo.py
```

Outputs CSV `results_demo.csv` with YBCO, MgB2, H3S.
