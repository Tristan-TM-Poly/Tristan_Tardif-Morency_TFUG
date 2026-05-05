# HGFM Documentation Index

Status: `S3-documentation-architecture`.

This index is the reusable entry point for documenting TFUGA / AI-7 as coupled fractal-mycelial hypergraphs. It is designed to be readable by humans, parsable by tools, and auditable by EvidenceGate.

## Purpose

Turn the whole documentation space into a navigable HGFM system:

```text
idea -> document -> node -> hyperedge -> projector -> DCT++ packet -> EvidenceGate status
```

## Core files

| File | Role | Status |
|---|---|---|
| `HGFM_DOCUMENTATION_HYPERGRAPH_MAP.md` | Defines documentation hypergraphs, typed edges, and hyperedges | S3 |
| `HGFM_DOC_STYLE_GUIDE.md` | Defines writing rules, status ladder, AntiHype wording, DCT++ fields | S3 |
| `HGFM_DOCUMENTATION_GRAPH.graphml` | GraphML visualization seed for docs/canon/evidence/projectors | S3 |
| `HGFM_DOCUMENTATION_INDEX.md` | This entry point and reuse map | S3 |
| `HGFM_DOCUMENTATION_PROJECTORS.md` | Projector definitions for human, machine, proof, lab, product, canon views | S3 |
| `HGFM_DOCUMENTATION_EVIDENCE_SCHEMA.json` | Machine-readable evidence schema for documentation claims | S3 |
| `HGFM_DOCUMENTATION_CI_PROTOCOL.md` | Draft CI protocol for documentation linting, claim gates, and artifact export | S3 |

## Hypergraph layers

### Layer 0: Canon layer
Defines stable vocabulary, equations, status ladders, allowed claims, and blocked claims.

### Layer 1: Theory layer
Maps equations, assumptions, invariants, proof sketches, and counterexamples.

### Layer 2: Code layer
Maps modules, APIs, commands, test outputs, build artifacts, and reproducibility notes.

### Layer 3: Evidence layer
Maps claim -> evidence -> test -> uncertainty -> status.

### Layer 4: Lab layer
Maps theory/code claims to calibration, controls, replicates, uncertainty, and safety gates.

### Layer 5: Product/revenue layer
Maps product promise -> checkout -> receipt -> delivery -> support -> feedback.

### Layer 6: Visualization layer
Exports GraphML/JSON/AceKG/Gephi/NetworkX-ready views.

## Promotion law

Documentation can improve clarity and reusability, but cannot by itself promote a physical, financial, medical, industrial, or deployment claim.

```text
Documentation alone <= S3/T3
Real data or real receipt required for S4/T4
Independent reproduction required for S5/T5
Stable minimal fertile reuse required for S6/T6
```

## Reuse pattern

For every new TFUGA module, create:

1. a human summary;
2. a machine schema;
3. a proof/falsification table;
4. a DCT++ packet;
5. a GraphML view;
6. an EvidenceGate result;
7. a next least-action route.

## Hard law

Document fractally. Link mycelially. Project usefully. Verify brutally. Canonize rarely.
