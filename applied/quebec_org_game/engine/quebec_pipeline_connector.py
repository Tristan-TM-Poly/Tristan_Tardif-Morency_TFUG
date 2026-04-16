import json
from pathlib import Path


def load_pipeline_config(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ingest_sources(config_path):
    config = load_pipeline_config(config_path)
    datasets = {}

    for source in config.get("sources", []):
        path = Path(source["path"])
        files = list(path.glob("*.csv")) if path.exists() else []
        datasets[source["name"]] = [str(f) for f in files]

    return datasets


def build_real_dataset_snapshot(config_path):
    datasets = ingest_sources(config_path)
    return {
        "datasets": datasets,
        "dataset_count": len(datasets)
    }
