# TRISTAN2_V6_SCHEMA_FAMILY — Applied Snapshot (2026-04-14)

## Core schema family
- `state.json`
- `score.json`
- `review.json`
- `validation.json`
- `propagation.json`
- `rollback.json`
- `contradiction.json`
- `sync.json`

## Expected law
Every major TRISTAN2 mutation path should be representable through a bounded subset of this schema family.

## Immediate purpose
The schema family exists to make Runtime V6 packetization explicit enough for implementation and audit.

## Constraint
Schema growth is valid only when it improves closure and replayability more than it increases complexity bulk.
