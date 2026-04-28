# AI-7 Institutional HyperAtlas Validation Runbook

This runbook defines the safe validation path for the Québec-Canada Institutional HyperAtlas.

## Local checks

Run gates on any JSON records before promotion:

```bash
python institutional_hyperatlas/gates/privacy_gate.py path/to/records.json
python institutional_hyperatlas/gates/license_gate.py path/to/records.json
```

## Promotion checklist

- Source exists.
- Licence or usage terms are known.
- Provenance is stored.
- Record is institution-level by default.
- Personal-data flags are reviewed before use.
- Outreach is manual-review only.
- No secrets are present.
- Cloud deployment is manual and reversible.

## PR #14 blocker

The Top 64^4 seed PR should not be merged into main until mixed Vercel status is resolved or explicitly reviewed.

## Next CI step

Add a workflow that runs only schema and gate tests. It must not fetch remote data, publish artifacts, or deploy cloud resources.
