# EXECUTABLE_TRACE_WIRING_PLAN — Applied Snapshot (2026-04-14)

## Purpose
Connect the staged Fractal-Loop executable trace placeholder to the governed review, score, benchmark, and promotion layers.

## Wiring sequence
1. executable trace placeholder produces a machine-readable trace object
2. trace object feeds the reduced-trace benchmark row
3. benchmark row feeds review summary updates
4. review summary feeds promotion decision row
5. promotion decision row remains bounded until rollback compatibility is preserved

## Required runtime hooks
- trace emitter
- artifact path recorder
- score update hook
- review update hook
- promotion gate hook

## Non-goal
This plan does not yet claim full runtime closure. It stages the shortest honest path from placeholder execution to governed interpretation.
