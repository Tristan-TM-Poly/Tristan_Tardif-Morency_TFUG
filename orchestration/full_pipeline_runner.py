from __future__ import annotations

import json
from pathlib import Path
from zip_governance.google_drive_real_download import GoogleDriveRealDownload
from zip_governance.drive_zip_inventory import scan_for_zips
from zip_governance.zip_hash_dedup import deduplicate_zip_entries
from zip_governance.zip_content_analyzer import analyze_many
from zip_governance.zip_ai7_classifier import classify_all

STATE_PATH = Path('orchestration/pipeline_state.json')


def write_state(payload: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def run_full_pipeline(folder_id: str, target_dir: str, max_files: int = 100) -> dict:
    downloader = GoogleDriveRealDownload()
    downloaded = downloader.sync_folder(folder_id, target_dir, max_files=max_files)

    entries = scan_for_zips(target_dir)
    dedup = deduplicate_zip_entries(entries)
    analysis = analyze_many(dedup['unique_entries'])
    classes = classify_all(dedup['unique_entries'])

    state = {
        'status': 'completed',
        'downloaded_count': len(downloaded),
        'inventory_count': len(entries),
        'unique_count': dedup['unique_count'],
        'duplicate_count': dedup['duplicate_count'],
        'analysis_count': len(analysis),
        'classification_count': len(classes)
    }
    write_state(state)
    return state
