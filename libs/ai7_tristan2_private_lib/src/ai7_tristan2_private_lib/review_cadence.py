from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ReviewEventType(str, Enum):
    VERSION = "version"
    AUTONOMY = "autonomy"
    PILOT = "pilot"
    CONTRADICTION = "contradiction"
    EXTERNAL_INGESTION = "external_ingestion"


@dataclass
class ReviewEvent:
    event_id: str
    event_type: ReviewEventType
    trigger: str
    required_outputs: List[str] = field(default_factory=list)


@dataclass
class ReviewCadence:
    events: List[ReviewEvent] = field(default_factory=list)

    def register(self, event: ReviewEvent) -> None:
        self.events.append(event)

    def list_by_type(self, event_type: ReviewEventType) -> List[ReviewEvent]:
        return [event for event in self.events if event.event_type == event_type]
