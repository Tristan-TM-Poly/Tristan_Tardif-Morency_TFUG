# T5 Binary Release Checklist - Axiom-Tristan Master v10

Target binary:

`axiom_tristan_master_zip_v10_2026_05_01.zip`

Current state:

- T3 for text publication index: canonical GitHub index, Drive index, and public mirror indexes exist.
- T2 for binary ZIP: local archive exists and source hash ledger exists, but the binary is not yet attached as an external asset.

## T5 requirements

A binary release reaches T5 only when all items below are satisfied.

### 1. Binary asset channel

Choose one channel:

- GitHub Release asset.
- Git LFS tracked file.
- Drive raw file upload.
- Other artifact storage with a stable URL and access control.

Record:

- Asset URL.
- Upload timestamp.
- Uploader/account.
- Access mode: public, private, or restricted.

### 2. Hash verification

Record the SHA-256 of the uploaded binary:

```bash
sha256sum axiom_tristan_master_zip_v10_2026_05_01.zip
```

Required check:

- Uploaded ZIP SHA-256 must match the master ledger.
- If it differs, do not promote to T5.

### 3. Download verification

A clean download test must be performed:

```bash
curl -L -o axiom_tristan_master_zip_v10_2026_05_01.zip '<ASSET_URL>'
sha256sum axiom_tristan_master_zip_v10_2026_05_01.zip
unzip -t axiom_tristan_master_zip_v10_2026_05_01.zip
```

Record:

- Terminal log.
- Result of `unzip -t`.
- Verifier identity or environment.

### 4. BAT record

Create or update a BAT record containing:

- Artifact name.
- Version: v10.
- Truth level: T5 only after successful external download verification.
- Asset URL.
- SHA-256.
- GitHub issue URL.
- Rollback instructions.

### 5. Rollback

Rollback must be possible.

Required rollback instructions:

- Delete or unpublish the release asset if incorrect.
- Mark issue #29 as not completed if verification fails.
- Keep text indexes, but downgrade binary status to T2.

### 6. Non-claims gate

Do not infer any of the following from binary publication:

- Cloud deployment.
- Patent/PCT/CIPO/arXiv/CRSNG filing.
- Experimental/physical validation.
- Revenue action.
- Purchase action.

Those require separate T5 receipts.

## Promotion rule

Promote the binary artifact to T5 only when:

```text
external_asset_url exists
AND uploaded_sha256 == expected_sha256
AND clean_download_sha256 == expected_sha256
AND unzip_test == OK
AND rollback_path exists
AND BAT_record exists
```

## Issue link

Canonical gate issue:

https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG/issues/29
