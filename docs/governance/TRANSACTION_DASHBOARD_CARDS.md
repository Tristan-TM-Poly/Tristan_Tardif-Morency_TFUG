# Transaction Dashboard Cards

Status: T3 dashboard card architecture.

Purpose: render revenue and purchase candidates as dashboard cards without executing financial actions or promoting transaction claims.

## Card fields

```text
card_id
transaction_id
transaction_type
current_tier
status
risk
blocked_actions
missing_evidence
human_approval_required
next_least_action
ledger_ref
```

## Revenue card: OmniSpectral R3 -> R4

```text
card_id: TX-CARD-REV-001
transaction_id: REV-DRAFT-001
transaction_type: revenue
current_tier: R3
status: draft
risk: medium until support/privacy/refund path and receipt evidence exist
blocked_actions: create payment link automatically; claim T4 without receipt; promise income
missing_evidence: real buyer or sponsor; receipt/sponsor log; delivery evidence; support contact; privacy/refund review
human_approval_required: yes
next_least_action: review private beta page and collect one approved reviewer/sponsor path
ledger_ref: outputs/transactions/revenue_ledger.jsonl
```

## Purchase card: future tool/service candidate

```text
card_id: TX-CARD-PUR-001
transaction_id: PUR-DRAFT-001
transaction_type: purchase
current_tier: P1
status: draft
risk: unknown until need, alternatives, budget, vendor and cancel/refund path are defined
blocked_actions: buy automatically; subscribe automatically; claim budget approval without review
missing_evidence: need definition; alternatives; budget ceiling; vendor/source review; cancellation/refund path
human_approval_required: yes
next_least_action: define purchase need and alternatives before any checkout
ledger_ref: outputs/transactions/purchase_ledger.jsonl
```

## Hard law

Dashboard cards are decision aids. They do not execute transactions.
