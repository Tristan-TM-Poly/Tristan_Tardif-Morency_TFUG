from __future__ import annotations

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
import os

class GoogleDriveRealDownload:
    def __init__(self, credentials_env: str = 'GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON') -> None:
        self.credentials_payload = os.environ.get(credentials_env)
        if not self.credentials_payload:
            raise RuntimeError('Missing GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON')
        self.creds = service_account.Credentials.from_service_account_info(eval(self.credentials_payload))
        self.service = build('drive', 'v3', credentials=self.creds)

    def list_files(self, folder_id: str, max_files: int = 100) -> list[dict]:
        query = f"'{folder_id}' in parents and trashed=false"
        result = self.service.files().list(q=query, pageSize=max_files, fields="files(id,name,mimeType)").execute()
        return result.get('files', [])

    def download_zip(self, file_id: str, target_dir: str) -> str:
        out = Path(target_dir)
        out.mkdir(parents=True, exist_ok=True)
        file_meta = self.service.files().get(fileId=file_id, fields='name').execute()
        file_name = file_meta['name']
        request = self.service.files().get_media(fileId=file_id)
        file_path = out / file_name
        with open(file_path, 'wb') as f:
            from googleapiclient.http import MediaIoBaseDownload
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        return str(file_path)

    def sync_folder(self, folder_id: str, target_dir: str, max_files: int = 100) -> list[str]:
        files = self.list_files(folder_id, max_files=max_files)
        downloaded = []
        for f in files:
            if f['mimeType'] == 'application/zip':
                path = self.download_zip(f['id'], target_dir)
                downloaded.append(path)
        return downloaded
