import time
from zip_governance.google_drive_real_download import GoogleDriveRealDownload
from zip_governance.zip_content_analyzer import analyze_many


def run_continuous(folder_id: str, target_dir: str, interval: int = 300, max_cycles: int = 10):
    downloader = GoogleDriveRealDownload()

    cycle = 0
    while cycle < max_cycles:
        print("[AUTO-RUNNER] Sync start")
        files = downloader.sync_folder(folder_id, target_dir)
        print(f"[AUTO-RUNNER] Downloaded: {len(files)} files")

        entries = [{'path': f} for f in files]
        analysis = analyze_many(entries)

        print("[AUTO-RUNNER] Analysis complete")
        print(analysis)

        cycle += 1
        print(f"[AUTO-RUNNER] Cycle {cycle}/{max_cycles}")
        time.sleep(interval)

    return {"status": "completed", "cycles": max_cycles}
