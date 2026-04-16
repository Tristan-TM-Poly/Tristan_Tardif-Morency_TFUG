from __future__ import annotations

from zip_governance.google_drive_download_impl import ApprovedGoogleDriveDownload


def run_sync(folder_id: str, target_dir: str):
    client = ApprovedGoogleDriveDownload()

    if not client.is_configured():
        return {'status': 'not_configured'}

    listing = client.list_target_folder(folder_id)

    # Placeholder: in real mode, iterate files and download ZIPs
    return {
        'status': 'ready',
        'listing': listing,
        'note': 'Download loop ready to plug with real API calls'
    }
