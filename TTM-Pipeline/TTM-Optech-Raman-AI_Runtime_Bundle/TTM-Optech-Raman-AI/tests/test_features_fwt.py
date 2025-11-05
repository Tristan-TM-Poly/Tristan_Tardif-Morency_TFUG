import numpy as np
from raman_ai.features.fwt import fwt_transform

def test_fwt_runs_on_sine():
    x = np.linspace(0, 1, 512)
    sig = np.sin(2*np.pi*50*x)
    coefs = fwt_transform(sig, wavelet='db4', level=3)
    assert coefs is not None
