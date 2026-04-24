from __future__ import annotations

from typing import Any


def build_storyboard(topic: str, steps: int = 3) -> dict[str, Any]:
    scenes = []
    for i in range(steps):
        scenes.append({
            "scene": i + 1,
            "description": f"Scene {i+1} about {topic}",
            "visual": "dynamic data visualization",
            "caption": f"Insight {i+1} on {topic}"
        })
    return {
        "topic": topic,
        "scenes": scenes
    }
