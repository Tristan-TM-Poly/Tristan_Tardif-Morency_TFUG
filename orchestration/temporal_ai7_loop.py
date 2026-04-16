from orchestration.memory_store import read_all, append_record
from orchestration.evolution_tracker import summarize_evolution


def run_temporal_update(profile_snapshot):
    history = read_all()
    append_record(profile_snapshot)
    updated_history = history + [profile_snapshot]
    evolution = summarize_evolution(updated_history)
    return evolution
