from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ApprovedGoogleDriveDownload:
    def __init__(self, credentials_env: str = 'GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON') -> None:
        self.credentials_env = credentials_env
        self.credentials_payload = os.environ.get(credentials_env)

    def is_configured(self) -> bool:
        return bool(self.credentials_payload)

    def load_credentials(self) -> dict[str, Any]:
        if not self.credentials_payload:
            raise RuntimeError('Missing GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON')
        return json.loads(self.credentials_payload)

    def list_target_folder(self, folder_id: str) -> dict[str, Any]:
        return {
            'folder_id': folder_id,
            'status': 'approved_listing_stub',
            'note': 'Replace stub with Google Drive API files.list implementation once runtime dependencies are approved.'
        }

    def approved_download_zip(self, file_id: str, target_dir: str) -> dict[str, Any]:
        out = Path(target_dir)
        out.mkdir(parents=True, exist_ok=True)
        placeholder = out / f'{file_id}.download.pending.json'
        placeholder.write_text(json.dumps({
            'file_id': file_id,
            'status': 'approved_download_stub',
            'note': 'Real media download requires approved API client install and authenticated request execution.'
        }, indent=2), encoding='utf-8')
        return {
            'file_id': file_id,
            'target_dir': str(out),
            'status': 'staged_stub',
            'placeholder': str(placeholder)
        }
