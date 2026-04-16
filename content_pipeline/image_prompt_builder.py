from __future__ import annotations

from typing import Any


def build_image_prompt(topic: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    mood = context.get("mood", "futuristic")
    style = context.get("style", "editorial scientific visualization")
    focus = context.get("focus", "networked intelligence system")
    prompt = f"{topic}, {focus}, {mood}, {style}, highly detailed, clean composition"
    return {
        "topic": topic,
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, distorted text, watermark",
    }
