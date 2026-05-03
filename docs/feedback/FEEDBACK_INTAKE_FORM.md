# Feedback Intake Form

Status: T3 feedback intake draft for human review.

Purpose: collect human, AI, beta, support, collaborator, PR, CI, and dashboard feedback in a consistent format so it can be routed into patches, tests, blocked claims, evidence requirements, or archived non-actions.

## Quick form

```text
Feedback ID:
Source type: human | ai | github | beta | support | ci | dashboard | collaborator | unknown
Source reference:
Summary:
Class: clarity | correctness | evidence | product | science | culture | governance | risk | other
Severity: S0 | S1 | S2 | S3 | S4
Suggested patch:
Required gate:
Evidence needed:
Status: new
Owner:
Next least action:
```

## Reviewer questions

1. What is unclear?
2. What feels overclaimed?
3. What evidence would make this credible?
4. What should be blocked until proof exists?
5. What is useful enough to keep?
6. What should be simplified?
7. What is the next smallest action?

## Routing hints

- Confusing wording -> clarity -> HumanReviewGate.
- Wrong statement or bug -> correctness -> CI / DCT++.
- Missing proof -> evidence -> EvidenceGate.
- Product objection -> product -> RevenueEvidenceGate.
- Raman or physics issue -> science -> EvidenceGate / S4Gate.
- Cultural/community concern -> culture -> KnowledgeRespectGate.
- Workflow, schema, dashboard issue -> governance -> UnifiedGovernanceCI.
- Safety, privacy, hype, misuse -> risk -> HumanReviewGate.

## Hard law

Feedback is input to improvement. It is not proof by itself.
