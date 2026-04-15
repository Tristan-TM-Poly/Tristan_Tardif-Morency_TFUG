from engine.ingest_seed_dataset import ingest
from engine.profile_engine import build_profiles
from engine.report_engine import summarize_profiles


if __name__ == "__main__":
    print("--- DEMO GAME LOOP ---")

    ingest("applied/quebec_org_game/data/seed_dataset.json")

    # Mock scoring input
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

    print("Profiles summary:")
    for org, data in summary.items():
        print(org, data)
