from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubRepoPointer:
    repository_full_name: str
    default_branch: str = "main"
    visibility: str = "private"

    def describe(self) -> str:
        return f"{self.repository_full_name} [{self.visibility}]@{self.default_branch}"
