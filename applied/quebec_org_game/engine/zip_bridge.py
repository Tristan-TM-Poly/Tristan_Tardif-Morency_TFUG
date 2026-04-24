from pathlib import Path


def list_zip_inputs(root):
    return list(Path(root).rglob("*.zip"))


def bridge_to_dataset(zips):
    print(f"Bridging {len(zips)} zip files into dataset pipeline")
