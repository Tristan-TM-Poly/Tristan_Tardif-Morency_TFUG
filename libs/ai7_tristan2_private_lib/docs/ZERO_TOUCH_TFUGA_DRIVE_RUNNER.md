# Zero-touch TFUGA Drive Runner

This packet adds a practical bridge between the private GitHub orchestration layer and the Drive-governed HGFM/T3 workflow.

## Goal
Run one bounded automation iteration against a Drive mirror or mounted Drive root:
- discover ZIP bundles
- extract them into a temporary workspace
- build inventories and pivot selections
- generate local HGFM graphs
- merge HGFM outputs
- assign T3 lanes
- emit governance decisions
- sync structured outputs back into Drive surfaces

## Why this lives here
The private library already defines the sovereign orchestration layer for Tristan, AI-7, TRISTAN2, Drive pointers, governance, and scoreboards. This runner acts as an executable bridge between that orchestration layer and the HGFM Automation Integration Packet already described in Drive.

## Outputs
The runner emits the following structures inside an output root:
- `manifests/zip_manifest.csv`
- `reports/inventory.csv`
- `reports/inventory.json`
- `genealogy/family_genealogy.json`
- `lanes/t3_lane_assignment.json`
- `hgfm/*_hgfm_local.json`
- `hgfm/hgfm_core_merged.json`
- `governance/promotion_decisions.json`
- `governance/review_queue.json`
- `governance/pilot_queue.json`
- `governance/archive_demotion.json`
- `reports/fusion_summary.json`
- `reports/drive_sync_log.json`

## Intended Drive surfaces
The default sync map writes to:
- `registry/zip_manifest.csv`
- `registry/inventory.csv`
- `registry/inventory.json`
- `genealogy/family_genealogy.json`
- `cockpit/t3_lane_assignment.json`
- `cockpit/fusion_summary.json`
- `cockpit/promotion_decisions.json`
- `cockpit/archive_demotion.json`
- `cockpit/review_queue.json`
- `cockpit/pilot_queue.json`
- `trunk/hgfm_core_merged.json`

## Execution modes
### Colab / mounted Drive
```bash
python libs/ai7_tristan2_private_lib/examples/zero_touch_tfuga_drive_runner.py \
  --drive-root "/content/drive/MyDrive/TFUGA_Autogoverned_Fusion" \
  --zip-input "incoming_zips" \
  --output "runs/latest"
```

### Local mirror
```bash
python libs/ai7_tristan2_private_lib/examples/zero_touch_tfuga_drive_runner.py \
  --drive-root "/path/to/local/mirror" \
  --zip-input "incoming_zips" \
  --output "runs/latest"
```

## Honesty boundary
This runner manages one bounded iteration. It does not claim to solve long-term credential management, cloud scheduling, or stronger cryptographic enforcement. Those should be layered later through a true runtime bus or service-account pipeline.
