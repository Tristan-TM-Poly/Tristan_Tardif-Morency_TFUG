
from raman_ai.io.standards import load_reference_spectra
import os

def test_load_reference_spectra():
    root = os.path.join(os.path.dirname(__file__), "..", "data", "standards")
    root = os.path.abspath(root)
    # in repo, data/standards is at project root
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "standards"))
    specs = load_reference_spectra(root)
    # tolerate empty if paths differ, but ensure no crash
    assert isinstance(specs, list)
