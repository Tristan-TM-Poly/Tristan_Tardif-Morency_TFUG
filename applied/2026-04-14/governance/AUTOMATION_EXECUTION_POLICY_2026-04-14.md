# AUTOMATION_EXECUTION_POLICY — Applied Snapshot (2026-04-14)

## Purpose
Define the fail-soft policy for the current automation frontier.

## Policy
- run the bundle from one governed entrypoint when possible
- preserve partial outputs even when some steps fail
- make failures visible in generated reports and digests
- prefer small auditable generated artifacts over opaque bulk output
- keep automation subordinate to frontier governance, not the reverse

## Primary entrypoint
- `applied/2026-04-14/runtime/run_automation_bundle_resilient_2026-04-14.py`

## Generated outputs
- resilient automation JSON report
- resilient automation markdown report
- automation digest
- generated artifact catalog

## Law
Automation is successful only when it increases governability, inspectability, and honesty about partial failure.
