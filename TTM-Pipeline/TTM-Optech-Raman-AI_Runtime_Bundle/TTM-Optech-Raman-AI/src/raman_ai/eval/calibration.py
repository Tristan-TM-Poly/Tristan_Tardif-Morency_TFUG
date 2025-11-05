import numpy as np
from dataclasses import dataclass

@dataclass
class IntervalCalibrationResult:
    nominal: float
    empirical: float
    miscalibration: float

def interval_coverage(y_true: np.ndarray, mu: np.ndarray, sigma: np.ndarray, conf: float = 0.90) -> IntervalCalibrationResult:
    # assume Gaussian predictive. coverage if |y - mu| <= z * sigma
    from scipy.stats import norm
    z = norm.ppf(0.5 + conf/2.0)
    inside = np.abs(y_true - mu) <= z * sigma
    emp = inside.mean()
    return IntervalCalibrationResult(nominal=conf, empirical=float(emp), miscalibration=float(emp - conf))

def ece_regression(y_true: np.ndarray, mu: np.ndarray, sigma: np.ndarray, n_bins: int = 10):
    # Expected Calibration Error for regression using normalized residuals
    # r = |y - mu| / sigma ~ HalfNormal(0,1) if calibrated.
    r = np.abs(y_true - mu) / (sigma + 1e-12)
    # Bin by predicted sigma (uncertainty buckets)
    edges = np.quantile(sigma.flatten(), np.linspace(0,1,n_bins+1))
    ece = 0.0
    for i in range(n_bins):
        mask = (sigma >= edges[i]) & (sigma <= edges[i+1])
        if mask.sum() == 0:
            continue
        # Ideal E[r] in half-normal is sqrt(2/pi) ~ 0.7979
        ideal = np.sqrt(2/np.pi)
        gap = np.abs(r[mask].mean() - ideal)
        ece += (mask.mean() * gap)
    return float(ece)


def isotonic_sigma_mapping(y_true, mu, sigma, n_quantiles: int = 15):
    """Calibre sigma par appariement de quantiles sur les résidus normalisés.
    Approche sans dépendance externe: piecewise-linear monotone mapping.
    Retourne une fonction f(s) ~ sigma_calibré.
    """
    y = np.asarray(y_true).flatten()
    m = np.asarray(mu).flatten()
    s = np.asarray(sigma).flatten() + 1e-12
    r = np.abs(y - m)  # résidu absolu

    # Bins par quantiles de sigma
    qs = np.linspace(0, 1, n_quantiles+1)
    edges = np.quantile(s, qs)
    centers = 0.5*(edges[:-1] + edges[1:])
    # Pour chaque bin, estimer sigma_cible = median(|y-m|) / median(|Z|) où Z~N(0,1)
    mask_list, tgt = [], []
    c_med = np.sqrt(2/np.pi)  # E|Z| pour Z~N(0,1), approx pour median robuste -> utilise corrige empirique:
    # Utilisons quantile 0.5 (médiane) cible pour |Z| ~ Half-Normal: med ≈ 0.67449
    med_halfnorm = 0.67448975
    for i in range(n_quantiles):
        lo, hi = edges[i], edges[i+1]
        msk = (s >= lo) & (s <= hi)
        if msk.sum() < 5:
            continue
        med_r = np.median(r[msk])
        tgt_sigma = med_r / med_halfnorm
        mask_list.append((lo, hi))
        tgt.append(tgt_sigma)
    if len(tgt) < 2:
        # fallback: échelle globale
        scale = np.median(r) / med_halfnorm / (np.median(s) + 1e-12)
        return lambda x: x * scale

    # Assurer monotonie en lissant par cummax
    centers = np.array([0.5*(a+b) for a,b in mask_list])
    tgt = np.maximum.accumulate(np.array(tgt))

    def f(x):
        xv = np.asarray(x).astype(float)
        # interp linéaire monotone
        return np.interp(xv, centers, tgt, left=tgt[0], right=tgt[-1])
    return f
