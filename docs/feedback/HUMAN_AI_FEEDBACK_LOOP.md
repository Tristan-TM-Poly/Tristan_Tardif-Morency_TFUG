# Human / AI Feedback Loop

Status: T3 feedback architecture for human review.

Purpose: convert comments, reviews, human opinions, AI critiques, private-beta feedback, GitHub PR discussion, and product objections into structured improvement packets without turning feedback into proof or truth automatically.

## Core law

Feedback improves direction. Evidence promotes status.

## Feedback equation

FeedbackLoop = Collect -> Classify -> De-risk -> Route -> Patch -> Test -> Review -> PromoteOrArchive.

## Feedback sources

- GitHub PR comments.
- Human reviewer notes.
- Private beta responses.
- AI critique / self-audit.
- User support questions.
- Product objections.
- Research collaborator comments.
- Classroom or lab feedback.
- Failed CI logs.
- Dashboard blockers.

## Feedback classes

- clarity: wording, explanation, positioning, onboarding.
- correctness: bug, false statement, wrong equation, wrong status.
- evidence: missing proof, missing data, missing receipt, missing permission.
- product: pricing, delivery, support, privacy, refund, beta response.
- science: data, uncertainty, calibration, controls, replicates, S4 readiness.
- culture: permission, attribution, review path, benefit-back, K-status.
- governance: CI, gate, schema, claim routing, status ceiling.
- risk: privacy, safety, overclaiming, misuse, hidden action.

## Human vs AI weighting

Human feedback can reveal usefulness, trust, confusion, ethics, product value, and real-world fit.

AI feedback can reveal consistency, missing files, structural gaps, contradiction, schema errors, and candidate improvements.

Neither human enthusiasm nor AI confidence is proof by itself.

## Feedback packet

Every useful comment should become a packet:

```text
feedback_id
source_type
source_ref
summary
class
severity
suggested_patch
required_gate
evidence_needed
status
owner
next_least_action
```

## Promotion rule

- positive comment = signal, not proof.
- repeated confusion = required clarity patch.
- bug report = test or issue.
- paid feedback / sponsor = possible T4 evidence if receipt exists.
- scientific criticism = EvidenceGate route.
- cultural/community concern = KnowledgeRespectGate route.

## Hard law

Listen to humans. Use AI to structure. Let gates decide status.
