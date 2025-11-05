
import numpy as np
from raman_ai.eval.calibration import isotonic_sigma_mapping

def test_isotonic_no_crash_and_monotone():
    rng = np.random.default_rng(0)
    y = rng.normal(size=128)
    mu = y + rng.normal(scale=0.1, size=128)
    sigma = np.abs(rng.normal(loc=0.5, scale=0.2, size=128)) + 1e-3
    f = isotonic_sigma_mapping(y, mu, sigma, n_quantiles=10)
    s2 = f(sigma)
    # monotone: if sigma sorted, s2 should be non-decreasing
    order = np.argsort(sigma)
    assert np.all(np.diff(s2[order]) >= -1e-9)
