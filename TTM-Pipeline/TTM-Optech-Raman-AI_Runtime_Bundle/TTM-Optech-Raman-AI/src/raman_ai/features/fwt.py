
import numpy as np

def extract(y, levels=4):
    y = np.asarray(y, dtype=float)
    out = {}
    cur = y.copy()
    for L in range(levels):
        energy = float(np.sum(cur**2))
        out[f"fwt_energy_L{L}"] = energy
        cur = (cur[::2] + 1e-9)
    return out
