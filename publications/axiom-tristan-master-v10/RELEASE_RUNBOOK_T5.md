# T5 Release Runbook - Axiom-Tristan Master v10

This runbook turns the binary release gate into an executable, auditable process.

## Current state

- Text/index publication: T3.
- Binary ZIP: T2 until externally uploaded and verified.
- Gate issue: https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG/issues/29

## Workflows

### Verify-only workflow

`.github/workflows/verify-axiom-tristan-master-v10-binary.yml`

Use when the ZIP is already hosted elsewhere and you only want a verification receipt.

Inputs:

- `asset_url`
- `expected_sha256`

Outputs:

- SHA check log.
- ZIP integrity log.
- Verification receipt artifact.

### Release workflow

`.github/workflows/release-axiom-tristan-master-v10-binary.yml`

Use when the ZIP is hosted elsewhere and should be verified, then attached to a GitHub Release.

Inputs:

- `asset_url`
- `expected_sha256`
- `tag_name`
- `release_name`
- `prerelease`

Outputs:

- GitHub Release with ZIP asset.
- Release receipt Markdown.
- Workflow receipt artifact.

## Promotion rule

Promote binary status to T5 only if:

```text
release workflow green
AND release asset exists
AND SHA-256 matches expected hash
AND unzip -t passed
AND receipt artifact exists
AND issue #29 is updated with release URL and verification log
```

## Rollback

If verification or release is wrong:

1. Delete or replace the incorrect release asset.
2. Keep the text indexes.
3. Keep issue #29 open.
4. Mark binary status as T2.
5. Re-run only after fixing source URL or expected SHA.

## Non-claims

A binary release does not imply:

- cloud deployment,
- official filing,
- experimental validation,
- purchase,
- revenue action.

Each requires its own gate and receipt.
