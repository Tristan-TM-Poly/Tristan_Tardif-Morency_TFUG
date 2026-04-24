from __future__ import annotations

from datetime import datetime
from typing import Any


def build_post(title: str, body: str, tags: list[str] | None = None) -> dict[str, Any]:
    return {
        "title": title,
        "body": body,
        "tags": tags or [],
        "created_at": datetime.utcnow().isoformat()
    }


def build_publication_manifest(posts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "post_count": len(posts),
        "posts": posts
    }
