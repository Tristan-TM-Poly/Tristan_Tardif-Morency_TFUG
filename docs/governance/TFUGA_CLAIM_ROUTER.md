# TFUGA Claim Router

Status: S3/T3/K3 governed routing architecture.

Purpose: route every claim produced by TFUGA / AI-7 / HGFM into the correct evidence gate before it can be promoted, published, sold, deployed, or canonized.

## Core equation

ClaimRoute(c) = Classify(c) -> RequiredGate(c) -> MaxStatus(c) -> MissingEvidence(c) -> NextLeastAction(c).

## Claim types

- science: physics, math, Raman, material, simulation, laboratory, instrument, validation.
- software: code, tests, CLI, package, local artifact, CI, reproducibility.
- revenue: product, pricing, checkout, sponsor, receipt, sales, passive/semi-passive income.
- cultural: community knowledge, place-based knowledge, language, translation, First Nations / Indigenous knowledge references.
- product: delivery manifest, support, refund, privacy, buyer promise, beta route.
- deployment: GitHub merge, Vercel, Drive publication, Stripe/payment, public launch, automation.
- governance: EvidenceGate, DCT++, HGFM docs, dashboards, propagation, review paths.

## Gate map

| Claim type | Required gate | Max status without external evidence |
|---|---|---|
| science | EvidenceGate / S4Gate | S3 |
| software | CI + DCT++ + reproducibility notes | S3 |
| revenue | RevenueEvidenceGate | T3 |
| cultural | KnowledgeRespectGate | K3 |
| product | ReleaseCandidateGate + RevenueEvidenceGate | T3 |
| deployment | HumanReviewGate + OfficialActionGate | T3 |
| governance | UnifiedGovernanceCI | S3/T3/K3 |

## Missing evidence rules

Science requires real data, metadata, controls, calibration, replicates, uncertainty, raw hashes, and reproduction path.

Revenue requires payment mechanism, real receipt or sponsor log, delivery evidence, support contact, refund/privacy review, and anonymized record.

Cultural/community knowledge requires public source or permission, attribution, review path, benefit-back, and no restricted or sensitive content.

Deployment requires explicit human approval, rollback, audit log, and external action evidence.

## Blocked routes

The router must block claims that assert:

- guaranteed passive income;
- physical validation without real data;
- autonomous deployment or payment control without review;
- cultural/community knowledge ownership, absorption, or replacement of knowledge holders;
- canon S6 without stable evidence and independent reproduction.

## Output packet

Every route emits:

```text
claim_id
claim_text
claim_type
required_gate
max_status_without_external_evidence
missing_evidence
blocked_claims
next_least_action
human_review_required
```

## Hard law

No claim reaches promotion directly. Every claim first passes through the router, then through its gate.
