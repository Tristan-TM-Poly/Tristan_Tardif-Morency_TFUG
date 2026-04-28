# JWST AI-7 Web/GitHub Absorption Protocol

## Principle

Use existing web, MAST, STScI, GitHub and scientific-tool resources as governed references before any download or reuse.

```text
resource -> registry -> licence/citation gate -> manifest -> local analysis -> DCT claim -> review
```

## Allowed by default

- Official documentation URLs.
- Official public archive pages.
- Public GitHub repositories as dependency references.
- Public notebooks as cited examples.
- Public or authorized JWST product manifests.

## Review required

- Bulk MAST download.
- Large calibration reference caches.
- HLSP products with collection-specific terms.
- Reusing notebook code beyond small cited patterns.
- Any proprietary or exclusive-access observations.

## Rejected by default

- Proprietary data without authorization.
- Uncited code copying.
- Unverified discovery claims.
- Treating enhanced images as scientific proof.
- Network access in no-network CI.

## Registry requirements

Every resource must declare:

```text
id, name, kind, url, use_for, ingest_mode, risk_level
```

## Canonical phrase

JWST-AI7 absorbs the existing scientific ecosystem as provenance, tools and manifests, not as uncontrolled bulk ingestion.
