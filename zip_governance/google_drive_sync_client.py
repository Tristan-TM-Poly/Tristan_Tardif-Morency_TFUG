from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class GoogleDriveSyncClient:
    def __init__(self, credentials_env: str = 'GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON') -> None:
        self.credentials_env = credentials_env
        self.credentials_payload = os.environ.get(credentials_env)

    def is_configured(self) -> bool:
        return bool(self.credentials_payload)

    def load_credentials(self) -> dict[str, Any]:
        if not self.credentials_payload:
            raise RuntimeError('Google Drive credentials not configured in environment')
        return json.loads(self.credentials_payload)

    def sync_manifest(self, manifest_path: str) -> dict[str, Any]:
        manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
        return {
            'configured': self.is_configured(),
            'folders': manifest.get('folders', []),
            'mode': manifest.get('mode', 'supervised_sync')
        }
