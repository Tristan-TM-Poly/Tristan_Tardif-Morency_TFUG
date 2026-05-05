# Human / AI Interaction Protocol

Status: T3 interaction architecture for human review.

Purpose: define how humans and AI agents should interact inside TFUGA / AI-7 / HGFM without turning AI output into unreviewed truth or turning human enthusiasm into evidence.

## Interaction modes

### Mode 1: Human asks, AI structures
Use for brainstorming, documentation, claims, outreach, and explanations.

Output: structured draft, not truth.

### Mode 2: AI critiques, human decides
Use for reviewing claims, detecting gaps, checking blocked language, and proposing patches.

Output: review suggestions, not automatic merge.

### Mode 3: Human reviews, AI patches
Use for PR comments, beta feedback, lab feedback, product objections.

Output: patch proposal, CI run, DCT++ update.

### Mode 4: AI routes, gates decide
Use for science/revenue/cultural/deployment claims.

Output: claim route, required gate, missing evidence, next action.

### Mode 5: Human approves external action
Use for merge, deploy, public launch, checkout/payment, outreach, Drive publication.

Output: explicit approval record and rollback path.

## Interaction packet

```text
interaction_id
human_or_ai_actor
intent
artifact_ref
claim_ref
feedback_ref
required_gate
action_allowed
action_blocked
next_step
review_status
```

## Allowed AI interaction actions

- summarize;
- classify;
- route claims;
- generate drafts;
- propose patches;
- run local/read-only checks;
- create dashboards;
- list missing evidence;
- prepare outreach drafts.

## Blocked AI interaction actions without explicit review

- merge;
- deploy;
- publish externally;
- create payment links;
- contact third parties;
- claim revenue;
- claim scientific validation;
- claim cultural/community permission;
- hide actions or logs.

## Hard law

Humans provide values, context, permission, and review. AI provides structure, speed, critique, and traceability. Gates provide promotion decisions.
