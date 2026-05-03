# Checkout T4 Evidence Protocol

Status: draft protocol. This file does not create a payment link or prove revenue.

## Purpose

Convert the first real checkout, sponsor, or paid delivery into a T4 evidence record without exposing private customer data.

## T4 minimum evidence

A revenue claim may move from T3 to T4 only when all are present:

- product artifact exists;
- delivery path exists;
- pricing page or offer exists;
- refund/support/privacy notes exist;
- human review approval exists;
- payment processor link or sponsor mechanism exists;
- first customer receipt or sponsor log exists;
- support contact exists;
- privacy/terms checked.

## Receipt record template

```yaml
product_id: omnispectral-evidencegate-starter-kit-v0.8
tier: Starter | Pro | Lab/Education
price_usd: 19 | 49 | 199
payment_provider: Stripe | GitHub Sponsors | other
receipt_id_hash: "sha256:..."
payment_timestamp_utc: "YYYY-MM-DDTHH:MM:SSZ"
delivery_manifest_version: v0.8
support_contact_available: true
refund_privacy_notes_version: v0.9
customer_identifier: anonymized
refund_status: none | requested | issued
support_issue_count: 0
```

## Privacy rule

Do not commit raw customer emails, names, addresses, payment details, private spectra, or personally identifying data. Commit only anonymized/hash records.

## Claim promotion rule

- 0 receipts: T3 maximum.
- 1 real receipt/sponsor log: T4 candidate.
- 3+ independent customers and repeat/retention evidence: T5 candidate.
- stable 30-90 day low-maintenance revenue: T6 candidate.
