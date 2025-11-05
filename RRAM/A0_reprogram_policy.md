# FRACTALE AI-7 — Policy for A0 Reprogramming and Refit

## Goal
Define automated decision thresholds and procedures to reprogram A0 (the high-precision background matrix)
while protecting RRAM endurance and ensuring operational stability.

## Key Signals to Monitor
- `contraction`: estimate of ||A0^{-1}|| * ||DeltaA||
- `residual_rel`: relative residual ||b - A x|| / ||b|| after Neumann iterations
- `drift_est`: measured drift from `measure_tile`
- `program_count`: cumulative programming operations per tile/cell (endurance budget)
- `temperature`: tile temperature

## Thresholds (suggested defaults)
- `contraction_reprogram` = 0.8   # if contraction >= this, plan reprogram
- `contraction_warn` = 0.6
- `residual_critical` = 1e-2
- `drift_threshold` = 0.05        # relative drift
- `program_budget_per_day` = 1000 # coarse estimate to preserve endurance

## Decision Procedure
1. **Periodic check (every supervision interval)**:
   - Estimate `contraction` via power method.
   - If `contraction < contraction_warn` → no action.
   - If `contraction_warn <= contraction < contraction_reprogram` → schedule maintenance window and consider partial promotion of high-energy ΔA sub-blocks into A0.
   - If `contraction >= contraction_reprogram` → trigger reprogram pipeline below.

2. **Reprogram pipeline**:
   - Validate `drift_est` and `temperature`. Abort if temperature > threshold.
   - Check program budget: if `program_count` for target tiles + estimated cost > budget, postpone and mark for manual maintenance.
   - Compute candidate new A0' = A0 + portion_of(DeltaA) chosen by energy metric (promote strongest ΔA columns/rows).
   - Simulate (digital) expected contraction for A0'. If improved (contraction down by >= 30%), commit to program_block calls (batched, plan-by-plan).
   - After programming, run verify (measure_tile) and run full Neumann solve to confirm residuals are within required tolerances.
   - If failure: rollback to previous A0 (use stored snapshot) and increase logging/alert.
3. **Emergency fallback**:
   - If residuals exceed `residual_critical` during operation, switch to digital fallback solver for affected tasks while scheduling reprogramming.

## Logging and Auditing
- Log every program_block call, pulse counts, final verify error, and the computed benefit (delta in contraction).
- Maintain snapshot versions of A0 (rolling snapshots) to enable rollback.