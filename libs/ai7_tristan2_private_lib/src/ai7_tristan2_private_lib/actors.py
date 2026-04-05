from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActorType(str, Enum):
    TRISTAN = "tristan"
    AI7 = "ai7"
    TRISTAN2 = "tristan2"
    CHATGPT = "chatgpt"
    DRIVE = "drive"
    UNKNOWN = "unknown"


_ALLOWED_ACTORS = {
    ActorType.TRISTAN,
    ActorType.AI7,
    ActorType.TRISTAN2,
    ActorType.CHATGPT,
    ActorType.DRIVE,
}


@dataclass(frozen=True)
class ActorProfile:
    actor_type: ActorType
    actor_id: str
    display_name: str
    is_privileged: bool = True


def is_actor_allowed(actor: ActorProfile) -> bool:
    return actor.is_privileged and actor.actor_type in _ALLOWED_ACTORS
