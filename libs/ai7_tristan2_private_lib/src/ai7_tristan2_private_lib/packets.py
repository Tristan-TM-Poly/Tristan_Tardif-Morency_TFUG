from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List


class PacketType(str, Enum):
    HUMAN = "human"
    MACHINE = "machine"
    AI = "ai"
    RESEARCH = "research"
    REVIEW = "review"
    PROPAGATION = "propagation"
    FALSIFICATION = "falsification"
    IMPLEMENTATION = "implementation"


@dataclass
class Packet:
    packet_id: str
    packet_type: PacketType
    title: str
    payload: Dict[str, Any] = field(default_factory=dict)
    links: List[str] = field(default_factory=list)


def packet_family_title(base_title: str, packet_type: PacketType) -> str:
    return f"{base_title} [{packet_type.value}]"
