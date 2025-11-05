
import numpy as np

def extract(x, y, mode="default"):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    def band(a,b):
        m = (x>=a)&(x<=b)
        return float(np.trapz(y[m], x[m])) if m.any() else 0.0
    a1 = band(495, 505)
    a2 = band(515, 525)
    r = (a2 + 1e-9) / (a1 + 1e-9)
    return {"ratio_520_500": float(r), "area_500": float(a1), "area_520": float(a2)}
