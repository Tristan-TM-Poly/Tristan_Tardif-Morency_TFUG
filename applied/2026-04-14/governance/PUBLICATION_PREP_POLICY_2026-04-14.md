# PUBLICATION_PREP_POLICY — Applied Snapshot (2026-04-14)

## Purpose
Define how the automatic publication-preparation layer should behave inside the governed TFUGA stack.

## Policy
- publication-prep outputs must remain derived from governed reports, digests, and writing stubs
- publication-prep must not promote frontier claims beyond benchmark and review evidence
- technical reporting remains upstream of publication-prep packaging
- generated publication-prep packages are staging artifacts, not final papers
- the publication-prep chain should remain auditable and CI-runnable

## Primary entrypoint
- `applied/2026-04-14/runtime/run_publication_prep_bundle_generated_2026-04-14.py`

## Expected outputs
- state of system
- publication prep package
- publication prep bundle reports

## Law
Publication-prep automation is successful only when it compresses governed reporting outputs into a more manuscript-ready layer without distorting the underlying frontier state.
