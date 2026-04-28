import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from jwst_ai7_lab.spectral import compute_redshift, line_snr, equivalent_width, velocity_offset
from jwst_ai7_lab.manifest import stage_from_filename
from jwst_ai7_lab.quality import QualityVector, quality_gate
from jwst_ai7_lab.dct import dct_claim_packet


def test_spectral_core():
    assert compute_redshift(2.0, 1.0) == 1.0
    assert line_snr([2, 3, 4], [1, 1, 1], [1, 1, 1]) > 0
    assert equivalent_width([1, 2, 3], [0.8, 0.8, 0.8], [1, 1, 1]) > 0
    assert velocity_offset(5.0, 5.0) == 0


def test_manifest_quality_dct():
    assert stage_from_filename('example_i2d.fits') == 'Stage 3 image'
    assert stage_from_filename('example_x1d.fits') == 'Stage 3 spectrum'
    assert quality_gate(QualityVector(calibration_known=True))['passed']
    packet = dct_claim_packet('candidate line detected', ['example_x1d.fits'])
    assert packet.promotion_status == 'candidate'
