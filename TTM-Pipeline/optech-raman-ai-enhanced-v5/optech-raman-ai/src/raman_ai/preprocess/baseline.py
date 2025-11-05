
import numpy as np

def _asls(y, lam=1e5, p=0.01, niter=10):
    L = len(y)
    D = np.diff(np.eye(L), 2)
    w = np.ones(L)
    for _ in range(niter):
        W = np.diag(w)
        Z = W + lam * D.T @ D
        z = np.linalg.solve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

def correct(x, y, method="asls"):
    y = np.asarray(y, dtype=float)
    if method == "asls":
        bl = _asls(y)
        return (y - bl)
    elif method == "airpls":
        bl = _asls(y, lam=1e5, p=0.01, niter=10)
        return (y - bl)
    else:
        return y
