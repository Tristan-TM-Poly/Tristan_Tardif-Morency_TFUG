
import numpy as np

def _sg(y, window=9, poly=3):
    if window < 3 or window % 2 == 0:
        window = 5
    k = window
    w = np.ones(k) / k
    return np.convolve(y, w, mode="same")

def apply(x, y, method="sg"):
    if method == "sg":
        return _sg(y)
    return y
