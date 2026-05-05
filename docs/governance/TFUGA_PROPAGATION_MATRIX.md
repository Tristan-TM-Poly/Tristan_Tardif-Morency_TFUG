# TFUGA Propagation Matrix

Status: S3/T3/K3 propagation architecture.

This matrix defines where each gate, artifact, and governance layer must propagate. It is designed to maximize reuse while preventing unsupported claims.

## Propagation matrix

| Layer | Propagate to | Required artifacts | Gate | Max status without external proof |
|---|---|---|---|---|
| HGFM documentation | docs/hgfm, CI artifacts, GraphML exports | index, projectors, schema, graph, CI protocol | HGFMDocGate | S3 |
| HyperRevenue | products/tfuga-hyper-revenue-reactor-v0.8, PR artifacts | product sheet, delivery manifest, pricing, claims register, T4 protocol | RevenueEvidenceGate | T3 |
| Knowledge Respect | docs/ethics, unified governance, review notes | protocol, schema, cultural claims register, CI gate | KnowledgeRespectGate | K3 |
| Unified Governance | .github/workflows, tools, PR comments | unified CI, read-only workflow, artifact upload | HumanReviewGate | S3/T3/K3 |
| Google Drive | publication briefs, evidence vault index, review records | brief, status, next actions, blocked claims | DriveReviewGate | S3/T3/K3 |
| Future releases | release candidate, private beta, package bundle | README, quickstart, DCT++, claim ledger, support notes | ReleaseCandidateGate | T3 |

## Propagation modes

### Mode A: Safe structure propagation
Allowed. Propagates protocols, schemas, gates, documentation, CI checks, and review paths.

### Mode B: Evidence propagation
Allowed if data or receipt exists. Propagates real evidence with privacy, consent, and hashing rules.

### Mode C: Claim propagation
Blocked unless EvidenceGate grants the appropriate level.

### Mode D: External action propagation
Requires explicit human review. Includes payment links, public launch, merge to main, deployment, Drive publication beyond briefs, or outreach.

## Minimum bundle for any new module

Every new module should include:

- status line;
- README or index;
- DCT++ report or packet;
- claims register;
- blocked claims;
- evidence or missing evidence;
- next least-action route;
- human review path;
- CI or manual validation checklist.

## Propagation priorities

1. Propagate unified governance into every reviewable module.
2. Propagate EvidenceGate into every claim-producing module.
3. Propagate KnowledgeRespectGate into every community/cultural/place-based knowledge reference.
4. Propagate RevenueEvidenceGate into every product, offer, pricing, checkout, or sponsorship artifact.
5. Propagate HGFM documentation projectors into every major doc.

## Hard law

Everywhere means every safe layer. It does not mean every external action.
