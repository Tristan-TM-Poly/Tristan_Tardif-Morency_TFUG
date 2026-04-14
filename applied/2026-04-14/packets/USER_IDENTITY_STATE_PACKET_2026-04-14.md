# USER_IDENTITY_STATE_PACKET — Applied Snapshot (2026-04-14)

## Purpose
Define the first bounded identity state packet for users across the TFUGA website, desktop app, and Android companion.

## State fields
- user_id
- public_display_name
- role
- membership_tier
- access_scope
- progression_state
- review_flags
- trust_state
- next_allowed_actions

## State transitions
- guest -> registered
- registered -> member
- member -> pro
- pro -> institutional
- any -> hold
- any -> rollback_review

## Law
Identity state is valid only if access, progression, and monetization remain auditable, role-bounded, and rollback-compatible.
