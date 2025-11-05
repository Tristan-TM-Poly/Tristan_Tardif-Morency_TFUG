# FRACTALE AI-7 — Hardware API Specification (minimal)

## Overview
This API is the firmware/SoC interface expected by the high-level AI-7 controller.
It exposes primitives for programming RRAM blocks, running matrix-vector multiplications (MVM),
calling the analog inverse block, and performing diagnostics/calibration.

## Primitives

### program_block(block_id: str, plan_id: int, G_matrix: ndarray) -> bool
- **Purpose:** Program a matrix (or tile) into the specified block and plan (bit-slice plane).
- **Arguments:**
  - `block_id`: identifier for A0/A1/A2/A3 or tile coordinate (e.g., "A0:tile(0,0)")
  - `plan_id`: integer plan index (0..P-1)
  - `G_matrix`: float32 ndarray of target normalized conductances (shape n x n)
- **Returns:** `True` on success, `False` on failure (detailed error in telemetry log)
- **Behavior:** use closed-loop incremental pulses + verify. Report programming steps and final error per cell.

### run_mvm(blocks_list: List[BlockDescriptor], input_vector: ndarray) -> ndarray
- **Purpose:** Compute the matrix-vector product over one or many blocks (bit-sliced)
- **Arguments:**
  - `blocks_list`: list of descriptors (block_id, plan_range, sign_mask info)
  - `input_vector`: float32 vector of voltages
- **Returns:** output_vector (float32) representing summed currents
- **Behavior:** the SoC will sequence ADC reads per plan and perform weighted accumulation. Apply sign-mask as needed.

### run_inverse(A0_descriptor: BlockDescriptor, b: ndarray) -> ndarray
- **Purpose:** Return approximate \(A_0^{-1} b\) using analog inverse hardware + digital refinement
- **Arguments:**
  - `A0_descriptor`: metadata describing A0 (tile layout, plans)
  - `b`: float32 vector
- **Returns:** approx solution vector (float32)
- **Behavior:** block may perform 1..k analog iterations; refine with FPGA numeric steps; should be deterministic and return residual metadata.

### measure_tile(tile_id: str) -> dict
- **Purpose:** Run diagnostic vectors for the tile and return measured effective conductances and drift estimates
- **Returns:** JSON dict: `{ "tile_id":..., "G_meas_summary":..., "drift_est":..., "temperature":..., "status": "ok" }`

### estimate_operator_norm(descriptor: BlockDescriptor, n_iter=20) -> float
- **Purpose:** Return estimated operator norm (spectral norm) using power method implemented on hardware (MVM calls)
- **Returns:** estimated float norm

## Telemetry / Logging
- Each call must emit structured telemetry: timestamps, call_id, duration, measured error statistics.
- Programming must log pulse counts per cell, final error, and verification pattern.

## Error codes
- `0` OK
- `1` Programming failure (excessive steps)
- `2` ADC failure
- `3` Temperature threshold exceeded
- `4` Tile readback mismatch

## Security and Safety
- Authentication of AI-7 controller to SoC.
- Rate-limits on program_block to protect RRAM endurance.
- Hardware interlocks for HV testing (require separate auth token).