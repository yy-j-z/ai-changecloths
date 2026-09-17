import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://ai_fitting:ai_fitting_dev@localhost:3306/ai_fitting",
    )
    ai_service_url: str = os.getenv("AI_SERVICE_URL", "http://localhost:8001")
    cors_origins_raw: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    llm_provider: str = os.getenv("LLM_PROVIDER", "demo")
    llm_model: str = os.getenv("LLM_MODEL", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


settings = Settings()
