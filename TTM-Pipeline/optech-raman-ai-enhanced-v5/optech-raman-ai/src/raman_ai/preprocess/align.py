
import numpy as np

def align_to_ref(x, y, ref_peak=520.7, max_shift=1.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    idx = np.argmax(y)
    x_peak = x[idx]
    delta = ref_peak - x_peak
    delta = np.clip(delta, -max_shift, max_shift)
    return x + delta, y
