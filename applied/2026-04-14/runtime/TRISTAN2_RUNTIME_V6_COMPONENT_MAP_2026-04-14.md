# TRISTAN2_RUNTIME_V6_COMPONENT_MAP — Applied Snapshot (2026-04-14)

## V6 target core
V6 = (Adapters, Queues, Workers, ArtifactEngine, ReviewEngine, PromotionEngine, HypergraphRegistry, DriftWatchers, EventStore, SyncStage, SafetyLayer)

## Component roles
- Adapters: Drive / ChatGPT / PC / Web routing
- Queues: command, packet, review, promotion, contradiction, sync
- Workers: bounded autonomous executors
- ArtifactEngine: standardized output family emitter
- ReviewEngine: machine-readable policy gate
- PromotionEngine: canon-safe branching and promotion logic
- HypergraphRegistry: node/edge/hyperedge and bridge serialization
- DriftWatchers: mismatch, staleness, unsupported claim, score drift, missing packet detectors
- EventStore: append-only event log and replay source
- SyncStage: staged export/import toward Drive-facing artifacts
- SafetyLayer: rollback, quarantine, autonomy gates, risk budgets

## Immediate implementation ladder
1. queue execution
2. artifact emission
3. event sourcing
4. review automation
5. reduced-model discipline
6. contradiction routing
7. hypergraph serialization

## Law
V6 should be treated as the first serious closure layer, not as an excuse for uncontrolled autonomy claims.
