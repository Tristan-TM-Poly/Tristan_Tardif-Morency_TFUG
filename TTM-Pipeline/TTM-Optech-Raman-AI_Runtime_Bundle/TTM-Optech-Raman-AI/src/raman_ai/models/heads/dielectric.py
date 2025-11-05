
import numpy as np

TARGETS = ["eps_r", "E_break", "rho_energy"]

def predict(features):
    x = np.array([
        features.get("tfuq_ms_energy_L0", 0.0),
        features.get("tfuq_ms_energy_L1", 0.0),
        features.get("ratio_520_500", 1.0),
    ], dtype=float)
    mu = np.array([10, 1e7, 1e3]) * (1 + 0.005*(x.mean() if x.size else 0.0))
    sigma = np.abs(mu) * 0.15 + 1e-6
    return dict(mu=mu.tolist(), sigma=sigma.tolist(), targets=TARGETS)
