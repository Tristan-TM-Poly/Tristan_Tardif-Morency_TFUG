
from pydantic import BaseModel
from typing import List, Optional, Dict

class RamanRecord(BaseModel):
    sample_id: str
    instrument_id: str
    laser_nm: int
    power_mw: float
    integration_s: float
    temp_C: float | None = None
    datetime: int | None = None  # epoch ms
    x_cm_1: List[float]
    y: List[float]
    y_pp: List[float] | None = None
    label_material: str | None = None
    y_targets: Dict[str, float] | None = None
    split: str | None = None


# --- Added: Pydantic data contracts (optional) ---
try:
    from pydantic import BaseModel, Field, validator
    class SpectrumRow(BaseModel):
        wavenumber: float = Field(..., description='Raman shift cm^-1')
        intensity: float = Field(..., description='Relative intensity (a.u.)')

        @validator('wavenumber')
        def _wn_gt0(cls, v):
            assert v >= 0, 'wavenumber must be >= 0 cm^-1'
            return v

        @validator('intensity')
        def _int_range(cls, v):
            # allow negatives if baseline not corrected yet, but cap extreme infinities
            assert abs(v) < 1e12, 'intensity out of bounds'
            return v
except Exception as _:
    SpectrumRow = None
