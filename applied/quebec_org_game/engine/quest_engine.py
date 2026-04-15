from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Quest:
    quest_id: str
    title: str
    objective: str
    difficulty: int
    reward: str


@dataclass
class QuestProgress:
    quest_id: str
    completed_targets: int
    total_targets: int

    def is_complete(self) -> bool:
        return self.completed_targets >= self.total_targets


class QuestEngine:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}

    def register_quest(self, quest: Quest):
        self.quests[quest.quest_id] = quest

    def generate_default_quests(self) -> List[Quest]:
        return [
            Quest("Q1", "Trace Funding", "Find funding relationships between 3 organizations", 2, "insight_points"),
            Quest("Q2", "Verify Event", "Validate an event using 2 independent sources", 3, "credibility_bonus"),
            Quest("Q3", "Resolve Conflict", "Resolve conflicting claims on an event", 4, "trust_score"),
        ]
