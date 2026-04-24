from engine.ingest_seed_dataset import ingest
from engine.profile_engine import build_profiles
from engine.report_engine import summarize_profiles
from engine.t3_profile_governance import apply_governance


if __name__ == "__main__":
    print("--- BOUNDED PILOT ---")

    ingest("applied/quebec_org_game/data/seed_dataset.json")

    events_by_org = {
        "org_demo_001": [
            {"dimension": "environment", "score": 2.0},
            {"dimension": "public_value", "score": 3.0}
        ],
        "org_demo_002": [
            {"dimension": "labour", "score": -2.5},
            {"dimension": "transparency", "score": -1.0}
        ]
    }

    profiles = build_profiles(events_by_org)
    summary = summarize_profiles(profiles)
    governance = apply_governance(profiles)

    print("Summary:")
    print(summary)

    print("Governance decisions:")
    print(governance)
