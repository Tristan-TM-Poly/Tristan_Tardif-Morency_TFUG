# ENTRYPOINT_DECISION_TABLE — Applied Snapshot (2026-04-14)

| Candidate | Class | Intended use | Stable visibility | Promotion requirement | Rollback note |
|---|---|---|---|---|---|
| `run_all.py` | sovereign-stable | daily governed execution | visible | maintain single-route clarity, packet coverage, review evidence | fallback remains available through lab path separation |
| `run_max_plus_ultra.py` | advanced-lab | bounded exploratory or high-intensity lab execution | hidden from daily trunk view | cannot seek stable status without packet/review/score closure | remains non-sovereign until explicit review |
| legacy ultra launchers | historical-lab | historical reference only | demoted | require explicit current-use pointer and review reason | default action is archive demotion |
| branch-specific ad hoc launchers | branch-local | bounded tests only | hidden | require launcher classification, pilot linkage, and rollback pointer | quarantine if ambiguity increases |

## Decision law
1. Exactly one sovereign stable entrypoint is visible at a time.
2. Advanced or historical launchers cannot claim equal status.
3. Launcher ambiguity is treated as governance debt.
4. Any candidate seeking promotion must improve clarity, not reduce it.
