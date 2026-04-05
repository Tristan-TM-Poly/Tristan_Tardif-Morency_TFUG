from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class DependencyGraph:
    edges: Dict[str, Set[str]] = field(default_factory=dict)

    def add_node(self, node: str) -> None:
        self.edges.setdefault(node, set())

    def add_dependency(self, node: str, depends_on: str) -> None:
        self.add_node(node)
        self.add_node(depends_on)
        self.edges[node].add(depends_on)

    def dependencies_of(self, node: str) -> List[str]:
        return sorted(self.edges.get(node, set()))

    def ready_nodes(self, completed: Set[str]) -> List[str]:
        ready: List[str] = []
        for node, deps in self.edges.items():
            if node in completed:
                continue
            if deps.issubset(completed):
                ready.append(node)
        return sorted(ready)
