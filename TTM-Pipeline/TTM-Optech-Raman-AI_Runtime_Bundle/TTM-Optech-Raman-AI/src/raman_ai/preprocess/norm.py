
import numpy as np

def apply(y, method="snv"):
    y = np.asarray(y, dtype=float)
    if method == "snv":
        mu = y.mean()
        sd = y.std() + 1e-9
        return (y - mu) / sd
    elif method == "area":
        a = y.sum() + 1e-9
        return y / a
    else:
        return y
