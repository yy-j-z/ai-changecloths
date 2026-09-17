from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)


class AdvisorRequest(BaseModel):
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=1000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)
    user_height_cm: float = Field(default=170, gt=80, lt=250)
    user_weight_kg: float = Field(default=65, gt=20, lt=300)


class ToolEvent(BaseModel):
    tool: str
    label: str
    status: Literal["completed", "failed"] = "completed"
    summary: str


class OutfitAction(BaseModel):
    garment_id: str
    garment_name: str
    size: str
    color: str
    color_hex: str


class AdvisorResponse(BaseModel):
    conversation_id: str
    reply: str
    state: Literal["needs_input", "completed", "failed"]
    tool_events: list[ToolEvent] = Field(default_factory=list)
    outfit_action: OutfitAction | None = None
