"""Configuration management using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="QGIS_TOOLKIT_",
        case_sensitive=False,
        extra="ignore",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="console", description="console or json")
    log_file: Path | None = Field(default=None, description="Optional log file path")

    # Processing
    max_workers: int = Field(default=4, ge=1, le=32, description="Parallel workers")
    chunk_size: int = Field(default=1000, ge=1, description="Processing chunk size")
    default_crs: str = Field(default="EPSG:4326", description="Default CRS")

    # Boulder analysis
    boulder_min_area: float = Field(default=1.0, gt=0, description="Min boulder area (m²)")
    boulder_max_area: float = Field(default=10000.0, gt=0, description="Max boulder area (m²)")
    boulder_height_threshold: float = Field(default=0.5, gt=0, description="Min height (m)")

    # Output
    output_dir: Path = Field(default=Path("./output"), description="Output directory")
    output_format: str = Field(default="geojson", description="geojson, shp, gpkg")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def reload_settings() -> Settings:
    """Force reload settings (useful in tests)."""
    get_settings.cache_clear()
    return get_settings()
