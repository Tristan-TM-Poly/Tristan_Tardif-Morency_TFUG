# HGFM Documentation Hypergraph Map

Status: `S3-documentation-architecture`.

This document defines how TFUGA / AI-7 documentation is represented as interconnected fractal-mycelial hypergraphs. It is documentation about documentation: a reusable map for organizing theory, code, tests, evidence, launch assets, and claims without letting any branch canonize itself.

## Canonical equation

```math
\mathcal{D}_{HGFM}
= EvidenceGate \circ DCT^{++} \circ \Pi_{docs} \circ FFWT_{docs} \circ Tensor_{docs} \circ Merge_{\Gamma}^{docs}(H_1,\ldots,H_N)
```

Where:

- `H_i` are documentation hypergraphs.
- `Merge_Gamma` couples documents through typed semantic edges.
- `Tensor_docs` extracts reusable latent documentation motifs.
- `FFWT_docs` reads documentation across scales: sentence, section, module, package, canon.
- `Pi_docs` projects the same documentation into human, machine, proof, lab, product, and canon views.
- `DCT++` attaches document, code, tests, risk, status, and missing evidence.
- `EvidenceGate` blocks unproven physical, financial, medical, or deployment claims.

## Documentation hypergraphs

### H0: Canon and definitions
Purpose: stable terms, definitions, equations, status ladder, AntiHype law.

Contains:
- TFUGA / AI-7 / HGFM / FTTE / OmniSpectral definitions;
- notation registry;
- S0-S6 and T0-T6 status scales;
- allowed and blocked claim classes.

### H1: Theory documentation
Purpose: equations, axioms, assumptions, invariants, derivations.

Contains:
- canonical equation;
- assumptions;
- domain of validity;
- proof sketches;
- falsifiers and counterexamples.

### H2: Code documentation
Purpose: modules, scripts, CLIs, tests, build commands.

Contains:
- module map;
- public APIs;
- command examples;
- test instructions;
- expected outputs.

### H3: Evidence documentation
Purpose: map claims to proofs, data, tests, uncertainty, and missing evidence.

Contains:
- claim ledger;
- evidence packets;
- DCT++ reports;
- raw data hashes;
- uncertainty budget;
- external reproduction status.

### H4: Lab protocol documentation
Purpose: translate claims into safe experimental requirements.

Contains:
- required data;
- calibration;
- blank/control requirements;
- replicate count;
- pass/fail criteria;
- safety notes.

### H5: Product and revenue documentation
Purpose: turn safe assets into reusable products without overclaiming.

Contains:
- product sheet;
- delivery manifest;
- support/refund/privacy notes;
- checkout evidence protocol;
- customer validation board.

### H6: Graph and visualization documentation
Purpose: export the documentation network into GraphML/JSON/Ace KG/Gephi-friendly forms.

Contains:
- nodes;
- typed edges;
- hyperedges;
- projectors;
- view presets.

## Typed edges

- `defines`: term -> definition.
- `depends_on`: module -> dependency.
- `supports`: evidence -> claim.
- `blocks`: missing evidence -> claim promotion.
- `tests`: protocol -> claim.
- `projects_to`: hypergraph -> representation view.
- `exports`: module -> artifact.
- `routes_to`: least-action route -> next action.
- `reuses`: package -> reusable component.
- `contradicts`: falsifier -> claim.

## Hyperedges

A documentation hyperedge links more than two artifacts:

```text
{claim, evidence, test, uncertainty, status}
{module, command, output, test_result}
{product, checkout, receipt, delivery, support}
{theory, equation, assumption, falsifier}
```

## Evidence law

```math
S4 \Rightarrow real\ data + metadata + controls + replicates + uncertainty.
```

Simulation, proxy output, or documentation alone cannot be promoted as physical validation.

## Hard law

Generate massively. Couple in parallel. Document fractally. Verify brutally. Canonize rarely.
