"""
SatyaNet - Configuration Module
Environment-driven settings using pydantic-settings.
"""
from functools import lru_cache
from typing import Dict

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    secret_key: str = Field(default="change_me_in_production", alias="SECRET_KEY")

    cloudinary_cloud_name: str = Field(default="", alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(default="", alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(default="", alias="CLOUDINARY_API_SECRET")
    cloudinary_upload_folder: str = Field(default="satyanet", alias="CLOUDINARY_UPLOAD_FOLDER")

    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="satyanet_evidence", alias="QDRANT_COLLECTION")

    nasa_firms_api_key: str = Field(default="", alias="NASA_FIRMS_API_KEY")
    openweather_api_key: str = Field(default="", alias="OPENWEATHER_API_KEY")

    weight_exif: float = Field(default=0.25, alias="WEIGHT_EXIF")
    weight_temporal: float = Field(default=0.20, alias="WEIGHT_TEMPORAL")
    weight_satellite: float = Field(default=0.25, alias="WEIGHT_SATELLITE")
    weight_duplicate: float = Field(default=0.20, alias="WEIGHT_DUPLICATE")
    weight_quality: float = Field(default=0.10, alias="WEIGHT_QUALITY")

    data_dir: str = Field(default="./data", alias="DATA_DIR")
    reports_dir: str = Field(default="./reports", alias="REPORTS_DIR")
    known_fakes_db: str = Field(default="./data/known_fakes.json", alias="KNOWN_FAKES_DB")

    @field_validator(
        "weight_exif",
        "weight_temporal",
        "weight_satellite",
        "weight_duplicate",
        "weight_quality",
    )
    @classmethod
    def _check_weight_range(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("Weight must be between 0.0 and 1.0")
        return v

    @property
    def weights(self) -> Dict[str, float]:
        """Return weight dict for truth score engine."""
        return {
            "exif_integrity": self.weight_exif,
            "temporal_plausibility": self.weight_temporal,
            "satellite_consistency": self.weight_satellite,
            "duplicate_check": self.weight_duplicate,
            "image_quality": self.weight_quality,
        }

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()