import json

import httpx
from pydantic import BaseModel, Field

from app.agents.contracts import AdvisorIntent


class IntentPayload(BaseModel):
    scene: str | None = None
    style: str | None = None
    budget: int | None = None
    excluded_colors: list[str] = Field(default_factory=list)


class CompatibleChatPlanner:
    """Intent planner for providers exposing a compatible chat-completions endpoint."""

    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.endpoint = f"{base_url.rstrip('/')}/chat/completions"
        self.api_key = api_key
        self.model = model

    def understand(self, message: str) -> AdvisorIntent:
        response = httpx.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "temperature": 0,
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Extract outfit intent as JSON with scene, style, budget and "
                            "excluded_colors. Use null for unknown values. Do not invent products."
                        ),
                    },
                    {"role": "user", "content": message},
                ],
            },
            timeout=15,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        payload = IntentPayload.model_validate(json.loads(content))
        return AdvisorIntent(
            scene=payload.scene,
            style=payload.style,
            budget=payload.budget,
            excluded_colors=tuple(payload.excluded_colors),
        )
