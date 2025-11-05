
import numpy as np

def moving_average(y, w=9):
    w = max(3, int(w))
    if w % 2 == 0: w += 1
    pad = w//2
    ypad = np.pad(y, (pad,pad), mode='edge')
    kernel = np.ones(w)/w
    return np.convolve(ypad, kernel, mode='valid')

def poly_baseline(x, y, deg=3, exclude_windows=None):
    m = np.ones_like(y, dtype=bool)
    if exclude_windows:
        for (a,b) in exclude_windows:
            m &= ~((x>=a)&(x<=b))
    coeff = np.polyfit(x[m], y[m], deg)
    base = np.polyval(coeff, x)
    return base, coeff

def integrate_band(x, y, window):
    a,b = window
    m = (x>=a)&(x<=b)
    if m.sum()<3:
        return np.nan
    return np.trapz(y[m], x[m])

def centroid(x, y, window):
    a,b = window
    m = (x>=a)&(x<=b)
    if m.sum()<3:
        return np.nan
    w = y[m] - y[m].min()
    w[w<0]=0
    if w.sum()==0:
        return np.nan
    return (x[m]*w).sum()/w.sum()

def fwhm_estimate(x, y, window):
    a,b = window
    m = (x>=a)&(x<=b)
    if m.sum()<5:
        return np.nan
    yy = y[m]
    xx = x[m]
    peak = yy.max()
    half = (peak + yy.min())/2.0
    above = yy>=half
    if above.sum()<2:
        return np.nan
    idx = np.where(above)[0]
    left = xx[idx[0]]
    right = xx[idx[-1]]
    return right - left
