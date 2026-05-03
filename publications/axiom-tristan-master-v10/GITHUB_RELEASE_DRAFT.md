# GitHub Release Draft - Axiom-Tristan Master v10

Tag:

`axiom-tristan-master-v10`

Title:

`Axiom-Tristan Master v10`

Attach binary:

`axiom_tristan_master_zip_v10_2026_05_01.zip`

## Release notes

Axiom-Tristan Master v10 consolidates the local Axiom-Tristan / TFUGA / AI-7 source archives, manifests, SHA-256 ledgers, BAT seed records, and safety gates.

Truth level at release creation:

- T3 for GitHub/Drive publication indexes.
- T5 for the binary ZIP only after the verification workflow passes with matching SHA-256 and ZIP integrity.

## Verification

After uploading the binary asset, run:

`.github/workflows/verify-axiom-tristan-master-v10-binary.yml`

Inputs:

```text
asset_url=<release-asset-url>
expected_sha256=<sha256-of-uploaded-zip>
```

The workflow must pass before binary promotion to T5.

## Non-claims

This release does not imply cloud deployment, official filing, experimental validation, purchase, or revenue action. Those require separate receipts and gates.

## Rollback

If verification fails, delete the release asset or mark the release pre-release/draft and keep issue #29 open.
