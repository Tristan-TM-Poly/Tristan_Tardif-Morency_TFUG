from pathlib import Path
import json

from applied.quebec_org_game.engine.quebec_real_data_adapter import build_dataset_index


def dataset_to_profiles(data_dir, config_path):
    index = build_dataset_index(data_dir, config_path)

    profiles = {}

    for dataset_id, files in index["datasets"].items():
        for f in files:
            org_key = dataset_id
            if org_key not in profiles:
                profiles[org_key] = {
                    "total_score": 0,
                    "events": []
                }

            profiles[org_key]["events"].append(f)
            profiles[org_key]["total_score"] += len(f)

    return profiles
