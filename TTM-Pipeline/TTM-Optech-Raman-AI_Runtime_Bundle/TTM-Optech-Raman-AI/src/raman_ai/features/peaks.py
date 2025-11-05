
import numpy as np

def _simple_peak_stats(x, y):
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    i = np.argmax(y)
    return {
        "peak_max": float(y[i]),
        "peak_pos": float(x[i]),
    }

def extract(x, y, mode="voigt"):
    return _simple_peak_stats(x, y)
