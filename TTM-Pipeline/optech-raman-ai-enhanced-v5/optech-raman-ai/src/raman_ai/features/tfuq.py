
import numpy as np

def _multiscale_stats(y, levels=5):
    y = np.asarray(y, dtype=float)
    out = {}
    cur = y.copy()
    for L in range(levels):
        out[f"tfuq_ms_energy_L{L}"] = float(np.sum(cur**2))
        out[f"tfuq_ms_mean_L{L}"]   = float(np.mean(cur))
        out[f"tfuq_ms_std_L{L}"]    = float(np.std(cur))
        # downsample (toy)
        cur = (cur[::2] + 1e-9)
    return out

def _psd_invariants(y):
    y = np.asarray(y, dtype=float)
    y = y - y.mean()
    Y = np.fft.rfft(y)
    psd = (Y*np.conj(Y)).real + 1e-12
    f = np.fft.rfftfreq(len(y), d=1.0)
    m = (f>0)
    xf = np.log(f[m])
    yf = np.log(psd[m])
    # linear fit slope (rough spectral exponent)
    A = np.vstack([xf, np.ones_like(xf)]).T
    slope, intercept = np.linalg.lstsq(A, yf, rcond=None)[0]
    return {
        "tfuq_psd_slope": float(slope),
        "tfuq_psd_intercept": float(intercept),
    }

def _quaternion_proxy(y):
    # Build a toy "Q = q0 + qi" proxy from amplitude/phase-like stats
    y = np.asarray(y, dtype=float)
    yc = y - y.mean()
    amp = np.linalg.norm(yc)
    # finite-diff phase proxy
    dy = np.diff(yc, prepend=yc[0])
    phase = float(np.arctan2(np.sum(dy[dy>0], dtype=float), 1.0 + np.sum(np.abs(dy), dtype=float)))
    q0 = float(amp)
    qi = float(phase)
    # norms and invariants
    norm2 = q0*q0 + qi*qi
    return {
        "tfuq_q0": q0,
        "tfuq_qi": qi,
        "tfuq_q_norm2": float(norm2),
        "tfuq_q_aniso": float(qi/(abs(q0)+1e-9))
    }

def extract(y, levels=5):
    out = {}
    out.update(_multiscale_stats(y, levels=levels))
    out.update(_psd_invariants(y))
    out.update(_quaternion_proxy(y))
    return out
