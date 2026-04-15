from pathlib import Path
import json


def load_drive_config(config_path):
    return json.loads(Path(config_path).read_text(encoding="utf-8"))


def match_datasets(files, config):
    matches = {}
    for dataset in config["datasets"]:
        if not dataset.get("enabled", True):
            continue
        dataset_id = dataset["dataset_id"]
        matches[dataset_id] = []
        for f in files:
            for pattern in dataset["expected_patterns"]:
                if pattern.replace("*", "") in f.name:
                    matches[dataset_id].append(str(f))
    return matches


def build_dataset_index(root_dir, config_path):
    root = Path(root_dir)
    files = list(root.rglob("*"))
    config = load_drive_config(config_path)
    matches = match_datasets(files, config)

    index = {
        "datasets": matches,
        "file_count": len(files)
    }

    return index
