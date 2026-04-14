from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class BusEvent:
    corridor: str
    object_id: str
    stage: str
    next_action: str


class RuntimeBusStub:
    def __init__(self) -> None:
        self.events: List[BusEvent] = []

    def emit(self, corridor: str, object_id: str, stage: str, next_action: str) -> None:
        self.events.append(BusEvent(corridor=corridor, object_id=object_id, stage=stage, next_action=next_action))

    def export(self) -> List[Dict[str, Any]]:
        return [asdict(e) for e in self.events]


def run_stub() -> Dict[str, Any]:
    bus = RuntimeBusStub()
    bus.emit("monitoring", "monitor.raman.process.001", "signal_checked", "route_if_breach")
    bus.emit("contradiction", "monitor.raman.process.001", "contradiction_emitted", "review_queue")
    bus.emit("promotion", "ai7.centrale.enriched.001", "gate_checked", "hold")
    return {
        "artifact_type": "ai7_tristan2_runtime_bus_stub",
        "events": bus.export(),
    }


if __name__ == "__main__":
    print(run_stub())
