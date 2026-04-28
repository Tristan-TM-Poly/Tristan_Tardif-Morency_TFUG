import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from jwst_ai7_lab.spectral import compute_redshift, line_snr, equivalent_width, velocity_offset
from jwst_ai7_lab.manifest import stage_from_filename
from jwst_ai7_lab.quality import QualityVector, quality_gate
from jwst_ai7_lab.dct import dct_claim_packet
from jwst_ai7_lab.source_registry import validate_registry
from jwst_ai7_lab.line_catalog import candidate_line_matches, observed_wavelength


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


def test_source_registry_and_line_catalog():
    registry_path = ROOT / 'data_sources' / 'jwst_existing_resources_registry.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    result = validate_registry(registry)
    assert result['passed'], result
    assert result['resource_count'] >= 8
    assert abs(observed_wavelength(0.656281, 1.0) - 1.312562) < 1e-9
    matches = candidate_line_matches(2.0, z_min=0, z_max=20)
    assert any(m['line'] == 'H_alpha' for m in matches)
