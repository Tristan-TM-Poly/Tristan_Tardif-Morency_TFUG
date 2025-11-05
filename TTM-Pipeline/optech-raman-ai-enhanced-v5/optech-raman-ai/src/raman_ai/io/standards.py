import os
import csv
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ReferenceSpectrum:
    name: str
    wavenumber: List[float]
    intensity: List[float]

def load_reference_spectra(root: str) -> List[ReferenceSpectrum]:
    spectra = []
    if not os.path.isdir(root):
        return spectra
    for fn in sorted(os.listdir(root)):
        if not fn.lower().endswith(".csv"):
            continue
        path = os.path.join(root, fn)
        wn, inten = [], []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wn.append(float(row["wavenumber"]))
                inten.append(float(row["intensity"]))
        spectra.append(ReferenceSpectrum(name=os.path.splitext(fn)[0], wavenumber=wn, intensity=inten))
    return spectra


def load_reference_spectra_mode(root: str, mode: str = "synthetic"):
    """Load spectra from synthetic (default) or real templates.
    mode in {"synthetic","real"}.
    Reads optional <name>.meta.json files if present.
    """
    import json
    import glob
    import os
    if mode not in {"synthetic","real"}:
        raise ValueError("mode must be 'synthetic' or 'real'")
    base = root if mode == "synthetic" else os.path.join(root, "real_templates")
    spectra = []
    metas = {}
    if not os.path.isdir(base):
        return spectra, metas
    for path in sorted(glob.glob(os.path.join(base, "*.csv"))):
        name = os.path.splitext(os.path.basename(path))[0]
        ref = load_reference_spectra(base)
        # reuse loader to read all, but filter by current file name
        # optimize: read directly
        import csv
        wn, inten = [], []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wn.append(float(row["wavenumber"])); inten.append(float(row["intensity"]))
        spectra.append(ReferenceSpectrum(name=name, wavenumber=wn, intensity=inten))
        meta_path = os.path.join(base, f"{name}.meta.json")
        if os.path.isfile(meta_path):
            try:
                with open(meta_path, "r") as fh:
                    metas[name] = json.load(fh)
            except Exception:
                metas[name] = {}
        else:
            metas[name] = {}
    return spectra, metas
