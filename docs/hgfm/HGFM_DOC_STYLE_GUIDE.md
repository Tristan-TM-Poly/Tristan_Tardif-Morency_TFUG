# HGFM Documentation Style Guide

Status: `S3-documentation-architecture`.

This guide defines how to write reusable documentation for hypergraphes fractales mycéliens (HGFM) without inflating claims.

## 1. Every document must declare a status

Use one of:

- `S0`: raw note;
- `S1`: speculative concept;
- `S2`: crystallizable draft;
- `S3`: local computable/software artifact;
- `S4`: real data with metadata, controls, replicates, and uncertainty;
- `S5`: independent reproduction;
- `S6`: stable minimal fertile canon.

## 2. Every major claim must have a claim class

Allowed classes:

- `definition`: naming and conceptual structure;
- `software`: local code, tests, outputs;
- `proxy`: computed proxy or simulation;
- `protocol`: required validation plan;
- `real-data`: real dataset with metadata;
- `external-reproduction`: independent validation.

Blocked unless evidence exists:

- physical/material validation;
- medical/industrial deployment;
- superconductivity;
- energy generation;
- autonomous lab control;
- guaranteed revenue.

## 3. Every technical doc should include DCT++ fields

Minimum fields:

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

## 4. Use the HGFM documentation pipeline

```text
concept
  -> definition
  -> hypergraph map
  -> tensor/proof map
  -> FFWT multiscale view
  -> projectors
  -> least-action next route
  -> DCT++ packet
  -> EvidenceGate status
```

## 5. Write for multiple projectors

Each document should be projectable into:

- human view: clear summary;
- machine view: structured JSON/GraphML-ready data;
- proof view: assumptions, claims, falsifiers;
- lab view: data and tests required;
- canon view: status and promotion blockers;
- product view: reusable artifact and safe promise.

## 6. Use AntiHype language

Prefer:

- `candidate`, `proxy`, `hypothesis`, `protocol`, `local artifact`, `requires validation`.

Avoid unless proven:

- `validated`, `proven`, `guaranteed`, `autonomous`, `infinite`, `physical proof`, `revenue guaranteed`.

## 7. Hard law

Document fractally. Link mycelially. Verify brutally. Canonize rarely.
