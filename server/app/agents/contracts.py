from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AdvisorIntent:
    scene: str | None
    style: str | None
    budget: int | None
    excluded_colors: tuple[str, ...] = ()


class IntentPlanner(Protocol):
    """Provider boundary for an LLM-backed or deterministic intent planner."""

    def understand(self, message: str) -> AdvisorIntent: ...
