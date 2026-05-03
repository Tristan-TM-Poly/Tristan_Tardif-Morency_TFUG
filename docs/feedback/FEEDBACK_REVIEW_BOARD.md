# Feedback Review Board

Status: T3 feedback board for human review.

Purpose: keep human and AI feedback actionable, traceable, and evidence-gated.

## Board columns

| ID | Source | Class | Severity | Summary | Required gate | Status | Next action |
|---|---|---|---|---|---|---|---|
| FB-001 | human | clarity | S2 | Public profile must be understandable in 30 seconds. | HumanReviewGate | new | Ask 5 reviewers if positioning is clear. |
| FB-002 | ai | governance | S2 | ClaimRouter should classify all public claims before posting. | ClaimRouterGate | new | Run router on public posts before publication. |
| FB-003 | beta | product | S3 | Product promise may be too abstract. | RevenueEvidenceGate | new | Test landing copy with 5 private reviewers. |
| FB-004 | ci | correctness | S3 | Failing workflow blocks release candidate readiness. | UnifiedGovernanceCI | new | Inspect CI logs and patch. |
| FB-005 | collaborator | science | S4 | Raman validation needs real data and uncertainty. | EvidenceGate / S4Gate | new | Prepare S4-ready Raman evidence packet. |
| FB-006 | human | culture | S4 | Any First Nations/community knowledge reference needs review path. | KnowledgeRespectGate | new | Keep only public summaries unless permission exists. |

## Severity scale

- S0: note only.
- S1: improvement idea.
- S2: clarity or usability issue.
- S3: blocker for release candidate.
- S4: blocker for claim promotion.

## Feedback-to-patch law

Every repeated feedback theme should either produce:

- a documentation patch;
- a code/schema/test patch;
- a blocked claim;
- a new evidence requirement;
- or an archived non-action with reason.

## Hard law

Feedback is signal. Repeated feedback is priority. Evidence is promotion.
