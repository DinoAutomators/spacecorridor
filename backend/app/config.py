from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


class Settings:
    """Simple environment-backed settings."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        default_data_path = project_root / "processed_data"
        self.project_root = project_root
        self.data_path = Path(os.getenv("CORRIDORIQ_DATA_PATH", default_data_path))
        raw_cors_origins = os.getenv("CORRIDORIQ_CORS_ORIGINS", "*")
        self.cors_origins = [origin.strip() for origin in raw_cors_origins.split(",") if origin.strip()]
        self.app_name = "CorridorIQ API"
        self.app_version = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
