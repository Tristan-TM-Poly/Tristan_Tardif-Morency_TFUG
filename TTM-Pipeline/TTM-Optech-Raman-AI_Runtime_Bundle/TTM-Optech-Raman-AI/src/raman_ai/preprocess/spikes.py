
import numpy as np

def remove_spikes(y, k=3, win=5):
    y = np.asarray(y, dtype=float)
    med = np.median(y)
    mad = np.median(np.abs(y - med)) + 1e-9
    z = (y - med) / (1.4826 * mad)
    ys = y.copy()
    mask = np.abs(z) > k
    for i in np.where(mask)[0]:
        a = max(0, i - win)
        b = min(len(y), i + win + 1)
        ys[i] = np.median(y[a:b])
    return ys.astype(y.dtype)
