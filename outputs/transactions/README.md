# Transaction Ledgers

Status: T3 generated-ledger structure.

Purpose: provide append-only style transaction ledgers for revenue and purchase candidates without claiming executed revenue, purchases, receipts, sponsors, refunds, or subscriptions.

## Files

- `revenue_ledger.jsonl`: revenue, sponsor, checkout, delivery, and receipt candidates.
- `purchase_ledger.jsonl`: purchase, quote, cart, subscription, and equipment/service candidates.

## Ledger law

A ledger entry records status. It does not create revenue or authorize spending.

## Required fields

```text
transaction_id
transaction_type
status
tier
description
amount_or_price
evidence_ref
human_approval_ref
blocked_actions
next_least_action
created_at
```

## Status constraints

- Draft entries are allowed.
- Review entries require a reviewer or approval path.
- Executed entries require real evidence references.
- No T4 revenue claim without receipt or sponsor log.
- No purchase execution without explicit human approval.

## Hard law

Logs are not money. Receipts are evidence. Human approval gates execution.
