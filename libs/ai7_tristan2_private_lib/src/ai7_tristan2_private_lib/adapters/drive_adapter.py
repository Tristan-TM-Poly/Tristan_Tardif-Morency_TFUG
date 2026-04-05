from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoogleDriveDocPointer:
    document_id: str
    kind: str = "document"

    def url(self) -> str:
        if self.kind == "spreadsheet":
            return f"https://docs.google.com/spreadsheets/d/{self.document_id}"
        if self.kind == "presentation":
            return f"https://docs.google.com/presentation/d/{self.document_id}"
        return f"https://docs.google.com/document/d/{self.document_id}"
