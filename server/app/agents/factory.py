from app.agents.compatible_planner import CompatibleChatPlanner
from app.agents.contracts import IntentPlanner
from app.agents.demo_planner import DemoIntentPlanner
from app.core.config import settings


def create_intent_planner() -> IntentPlanner:
    if settings.llm_provider == "demo":
        return DemoIntentPlanner()
    if settings.llm_provider == "compatible":
        if not settings.llm_base_url or not settings.llm_model or not settings.llm_api_key:
            raise RuntimeError(
                "LLM_BASE_URL, LLM_MODEL and LLM_API_KEY are required for compatible provider"
            )
        return CompatibleChatPlanner(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
