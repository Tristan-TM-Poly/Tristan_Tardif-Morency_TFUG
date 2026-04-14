# TRISTAN2_V6_SCHEMA_EXAMPLES — Applied Snapshot (2026-04-14)

## Example subset
### `state.json`
```json
{"object_id":"pilot.fractal_loop.001","stage":"bounded","status":"active"}
```

### `score.json`
```json
{"object_id":"ai7.centrale.enriched.001","score":{"resilience":8,"safety":7,"knowledge":8}}
```

### `review.json`
```json
{"object_id":"pilot.raman.001","review_state":"staged","next_gate":"dataset_bound_attachment"}
```

### `contradiction.json`
```json
{"object_id":"monitor.raman.process.001","trigger":"observable_threshold_breach","next_action":"route_to_review_queue"}
```

### `rollback.json`
```json
{"object_id":"ai7.centrale.enriched.001","rollback_pointer":"hold_and_quarantine","reason":"safety_drift"}
```

## Law
Schema examples are valid only if they clarify implementation and replayability without pretending that the full runtime bus already exists.
