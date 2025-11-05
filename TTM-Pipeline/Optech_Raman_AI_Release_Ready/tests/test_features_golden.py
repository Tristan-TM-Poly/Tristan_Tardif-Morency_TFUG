import pandas as pd, numpy as np
from pathlib import Path
from scipy.signal import find_peaks

# Minimal physics features (local, to avoid import complexity)
def features_physics(df, prominence=0.01, distance=5, topk=5):
    x = df["wavenumber_cm1"].to_numpy()
    y = df["intensity"].to_numpy()
    peaks, props = find_peaks(y, prominence=prominence, distance=distance)
    # sort by prominence desc
    prom = props.get("prominences", np.zeros_like(peaks))
    order = np.argsort(prom)[::-1]
    peaks = peaks[order]
    x0 = x[peaks[0]] if len(peaks)>0 else np.nan
    return {"first_peak_pos": float(x0)}

def load_csv(p: Path):
    return pd.read_csv(p)

def test_si_peak_near_520():
    df = load_csv(Path(__file__).parent / "golden_data" / "si_520.csv")
    feats = features_physics(df, prominence=0.02, distance=5, topk=1)
    assert 510 <= feats["first_peak_pos"] <= 530, f"expected ~520 cm^-1, got {feats['first_peak_pos']}"

def test_polymer_peak_near_1001():
    df = load_csv(Path(__file__).parent / "golden_data" / "polymer_1001.csv")
    feats = features_physics(df, prominence=0.02, distance=5, topk=1)
    assert 990 <= feats["first_peak_pos"] <= 1010, f"expected ~1001 cm^-1, got {feats['first_peak_pos']}"
