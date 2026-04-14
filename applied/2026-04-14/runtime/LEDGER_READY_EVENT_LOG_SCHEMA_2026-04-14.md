# LEDGER_READY_EVENT_LOG_SCHEMA — Applied Snapshot (2026-04-14)

## Minimal fields
- event_type
- object_name
- artifact_pointer
- verdict
- review_pointer
- promotion_pointer
- owner
- timestamp_placeholder

## First intended events
- trace_artifact_emitted
- benchmark_row_updated
- review_row_updated
- promotion_decision_checked

## Law
The event log schema stays useful only if it remains smaller than the frontier it tries to govern.
