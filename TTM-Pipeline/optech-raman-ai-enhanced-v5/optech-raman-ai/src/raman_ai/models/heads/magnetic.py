
import numpy as np

TARGETS = ["anisotropy_eff", "coercivity"]

def predict(features):
    x = np.array([
        features.get("tfuq_q_aniso", 0.0),
        features.get("psd_slope", features.get("tfuq_psd_slope", 0.0)),
    ], dtype=float)
    mu = np.array([0.5, 100]) * (1 + 0.02*(x.mean() if x.size else 0.0))
    sigma = np.abs(mu) * 0.2 + 1e-6
    return dict(mu=mu.tolist(), sigma=sigma.tolist(), targets=TARGETS)
