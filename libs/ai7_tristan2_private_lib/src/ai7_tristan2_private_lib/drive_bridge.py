from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class DrivePointer:
    provider: str
    file_id: str
    url: str
    mime_type: str = ""


@dataclass
class DrivePayload:
    pointer: DrivePointer
    privacy_scope: str = "private"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_record(self) -> Dict[str, Any]:
        return {
            "provider": self.pointer.provider,
            "file_id": self.pointer.file_id,
            "url": self.pointer.url,
            "mime_type": self.pointer.mime_type,
            "privacy_scope": self.privacy_scope,
            "metadata": self.metadata,
        }
