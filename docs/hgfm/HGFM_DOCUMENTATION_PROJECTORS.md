# HGFM Documentation Projectors

Status: `S3-documentation-architecture`.

Projectors turn the same documentation hypergraph into different useful representations. A projector does not canonize; it only renders a view. EvidenceGate decides promotion.

## Projector equation

```math
P_k: H_{docs} \rightarrow R_k
```

Where `H_docs` is the documentation hypergraph and `R_k` is a representation optimized for a use case.

## P_human

Purpose: make a document quickly understandable.

Output:

- one-sentence purpose;
- status level;
- what is allowed to claim;
- what is blocked;
- next least-action step.

## P_machine

Purpose: make documentation parsable by code.

Output:

- JSON keys;
- node IDs;
- edge types;
- schema links;
- artifact paths.

## P_proof

Purpose: expose proof structure.

Output:

- assumptions;
- claims;
- evidence;
- tests;
- falsifiers;
- missing evidence.

## P_lab

Purpose: translate a theory/code claim into experimental requirements.

Output:

- required data;
- metadata;
- calibration;
- blank/control;
- replicates;
- uncertainty budget;
- safety blockers.

## P_product

Purpose: translate a reusable artifact into a safe commercial/product page.

Output:

- safe promise;
- delivery manifest;
- support/refund/privacy notes;
- checkout evidence protocol;
- blocked revenue claims.

## P_canon

Purpose: decide whether a document belongs in stable canon, crystallizable branch, or exploration.

Output:

- promotion candidate;
- quarantine reason;
- archive reason;
- required evidence for next level.

## P_graph

Purpose: export visual and machine-readable structure.

Output:

- GraphML;
- JSON nodes and edges;
- hyperedges;
- visual clusters;
- external tool compatibility notes.

## Agreement score

```math
Agreement(P_1,\ldots,P_n)=1-\frac{1}{\binom n2}\sum_{i<j} Dist(P_i(H),P_j(H))
```

A document is stronger when human, machine, proof, lab, product, and canon projections agree.

## Promotion lock

```text
Projection agreement improves clarity.
EvidenceGate improves status.
Documentation alone cannot promote physical or revenue claims beyond S3/T3.
```
