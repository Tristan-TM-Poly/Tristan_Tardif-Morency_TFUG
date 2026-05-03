# HGFM Documentation CI Protocol

Status: `S3-documentation-architecture`.

This protocol defines how documentation changes should be checked before merge. It is PR/artifact oriented and does not auto-publish claims.

## Goals

- keep documentation reusable;
- detect unsupported claims;
- ensure DCT++ fields are present;
- export graph artifacts;
- keep PRs reviewable by humans.

## Suggested CI jobs

```text
hgfm-doc-lint
claim-ledger-check
evidence-schema-check
graphml-smoke-test
dctpp-field-check
blocked-claim-scan
```

## hgfm-doc-lint

Checks:

- every HGFM doc has a status line;
- every major doc declares purpose;
- every claim-heavy doc has allowed and blocked claims;
- every product/revenue doc has support/refund/privacy notes or references.

## claim-ledger-check

Checks:

- claims have status;
- claims have evidence or missing evidence;
- blocked claims are explicitly listed;
- no guaranteed revenue or physical validation claim appears without proof.

## evidence-schema-check

Checks `HGFM_DOCUMENTATION_EVIDENCE_SCHEMA.json` against sample evidence packets.

## graphml-smoke-test

Checks:

- GraphML is parseable XML;
- every edge source and target exists;
- relation fields are present.

## dctpp-field-check

Checks that docs include or reference:

```text
D: document/definition
C: code/calculation
T: test/protocol
E: energy/cost
S: stress/fragility
J: usefulness/joy/readability
R: risk
P: priority
sigma: status
K: links/proofs/missing evidence
```

## blocked-claim-scan

Blocks or flags risky phrases unless accompanied by explicit EvidenceGate status:

```text
guaranteed passive income
validated superconductivity
autonomous lab control
risk-free return
proven physical effect
infinite revenue
```

## Merge law

Docs can merge when they improve clarity and governance. They do not promote scientific, physical, financial, medical, or deployment claims without evidence.

## Hard law

CI assists review. Humans approve publication.
