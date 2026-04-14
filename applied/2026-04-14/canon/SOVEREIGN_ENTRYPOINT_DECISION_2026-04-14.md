# SOVEREIGN_ENTRYPOINT_DECISION — Applied Snapshot (2026-04-14)

## Decision
- Stable sovereign entrypoint candidate: `run_all.py`
- Advanced laboratory entrypoint candidate: `run_max_plus_ultra.py`

## Doctrine
The stable sovereign entrypoint is the single daily execution path used for governed runtime, review, score, and promotion logic.
The advanced laboratory entrypoint stays available for bounded exploratory work and must not be presented as equal to the sovereign path until promotion discipline is attached.

## Immediate consequences
1. Remove duplicate stable-route ambiguity.
2. Keep advanced launchers separated from daily trunk visibility.
3. Attach score/review/promotion evidence to any candidate seeking stable status.
4. Preserve rollback visibility for all non-sovereign launch paths.

## Review gate
Promotion beyond this decision requires:
- no duplicate entry routes for the same stable purpose
- one bounded pilot linked to the stable path
- packet completeness for the chosen path
- review evidence that launch clarity improved

## Applied note
This file stages the Drive-side decision into the repo without claiming final replacement of upstream canon artifacts.