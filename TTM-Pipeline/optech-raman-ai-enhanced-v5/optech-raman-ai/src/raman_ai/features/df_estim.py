
import numpy as np

def extract(y):
    y = np.asarray(y, dtype=float)
    y = y - y.mean()
    Y = np.fft.rfft(y)
    psd = (Y*np.conj(Y)).real + 1e-12
    f = np.fft.rfftfreq(len(y), d=1.0)
    m = (f>0)
    xf = np.log(f[m])
    yf = np.log(psd[m])
    A = np.vstack([xf, np.ones_like(xf)]).T
    slope, intercept = np.linalg.lstsq(A, yf, rcond=None)[0]
    df_proxy = 1.0 - 0.5*slope
    return {"df_proxy": float(df_proxy), "psd_slope": float(slope)}
