from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration.

    Keep it env-first so Terraform/Ansible (or docker compose) can inject values easily.
    """

    model_config = SettingsConfigDict(env_prefix="ADO_MOCK_", extra="ignore")

    # Server
    host: str = "0.0.0.0"
    port: int = 8080

    # Fixtures
    fixtures_path: str = "fixtures/demo.json"
    dataset: str = "demo"

    # API behavior
    strict_api_version: bool = False
    allowed_api_versions: str = "7.0,7.1-preview.1"
    artificial_latency_ms: int = 0

    # Auth
    auth_mode: str = "none"  # none | pat | bearer
    token: str = "local-dev-token"

    @property
    def allowed_versions(self) -> set[str]:
        return {v.strip() for v in self.allowed_api_versions.split(",") if v.strip()}
