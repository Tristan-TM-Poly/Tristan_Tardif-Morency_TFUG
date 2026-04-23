# TFUGA Output Contract

This directory contains generated outputs for the bounded canonical pilot and the zero-touch TFUGA workflow.

## Expected Artifacts
- `quebec_real_index.json`
- `canon_hook.json`
- `hgfm_graph.json`
- `hgfm_summary.json`

## Semantics
- `quebec_real_index.json`: index of ingested real or bootstrap datasets
- `canon_hook.json`: canonical handoff status for TFUGA
- `hgfm_graph.json`: exported graph view for visualization
- `hgfm_summary.json`: compact graph counts summary

## Important Note
This directory may be created by workflows or local runs. Artifacts can be ephemeral in CI and uploaded separately through GitHub Actions.
