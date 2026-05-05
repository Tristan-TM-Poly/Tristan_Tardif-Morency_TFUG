# Reusable Asset Packaging Protocol

Status: `T3-reusable-asset-protocol`.

This protocol turns every TFUGA / HGFM / OmniSpectral deliverable into a reusable asset package that can be reviewed, delivered, supported, and audited without inflating claims.

## Package equation

```text
ReusableAsset = Source + Demo + Docs + DCT++ + ClaimLedger + DeliveryManifest + SupportPolicy + EvidenceGate
```

## Minimum reusable package

Every paid or shareable package should contain:

- `README.md`: what it does and does not do;
- `QUICKSTART.md`: shortest path to first successful run;
- `EXAMPLES/`: demo inputs and expected outputs;
- `DCTPP_REPORT.md`: status, evidence, missing evidence;
- `CLAIMS_REGISTER.md`: allowed and blocked claims;
- `DELIVERY_MANIFEST.md`: exact buyer/user deliverables;
- `SUPPORT_REFUND_PRIVACY_NOTES.md`: support and safety boundaries;
- `VERSION.md`: package version and changelog;
- `LICENSE_OR_TERMS_NOTE.md`: draft license/terms note for human review.

## Reuse classes

- `R0`: one-off artifact;
- `R1`: reusable by creator;
- `R2`: reusable by collaborator;
- `R3`: reusable by customer/student;
- `R4`: reusable by institution/lab;
- `R5`: reusable as platform module.

## Promotion lock

```text
R3 requires a clear quickstart and delivery manifest.
R4 requires support, versioning, and classroom/lab fit.
R5 requires CI, schemas, tests, and stable API boundaries.
```

## Blocked claims

Reusable does not mean autonomous, guaranteed, validated, or revenue-producing by itself.

## Next least action

Convert the OmniSpectral EvidenceGate Starter Kit into an R3 candidate by adding a quickstart, demo input, expected output, and version note.
