from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "AI Agent Reliability & Support Platform"
    app_version: str = "0.1.0"
    environment: str = "development"
    service_name: str = "incident-support-api"
    gcp_project_id: str | None = None
    gcp_location: str = "us-central1"
    vertex_model: str = "gemini-2.5-flash"
    vertex_timeout_seconds: float = Field(default=25, gt=0, le=120)
    mock_mode: bool = False
    max_request_bytes: int = Field(default=32_768, ge=1024, le=1_000_000)
    enable_simulations: bool = False
    simulation_token: str | None = None
    event_history_size: int = Field(default=100, ge=10, le=1000)
    monitoring_dashboard_url: str | None = None
    logging_url: str | None = None

    @property
    def simulations_available(self) -> bool:
        return self.environment != "production" and self.enable_simulations and bool(self.simulation_token)


@lru_cache
def get_settings() -> Settings:
    return Settings()
