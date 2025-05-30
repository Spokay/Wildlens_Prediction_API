import os
import logging
import pathlib
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Environment
    environment: str = Field(default="development", description="Runtime environment")
    debug: bool = Field(default=True, description="Debug mode")
    app_port: int = Field(default=8000, description="Application port")

    # Wildlens API Configuration
    wildlens_prediction_api_key: Optional[str] = Field(
        default=None,
        description="Wildlens prediction API key",
        validation_alias="WILDLENS_PREDICTION_API_KEY"
    )

    # Model Paths
    wildlens_footprint_multiclass_classifier_model_path: Optional[str] = Field(
        default=None,
        description="Path to the multiclass classifier model",
        validation_alias="WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH"
    )
    wildlens_footprint_binary_classifier_model_path: Optional[str] = Field(
        default=None,
        description="Path to the binary classifier model",
        validation_alias="WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH"
    )

    # API Configuration
    api_prefix: str = Field(
        default="/api",
        description="Prefix for API routes"
    )

    # Computed properties
    @property
    def project_root(self) -> pathlib.Path:
        return pathlib.Path(__file__).resolve().parent.parent

    @property
    def excluded_paths(self) -> List[str]:
        # Paths that do not require authentication
        return [
            "/docs",
            "/openapi.json",
            "/metrics"
        ]

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def is_testing(self) -> bool:
        return self.environment.lower() == "testing"

    # Pydantic V2 field validators
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ['development', 'production', 'testing']
        if v.lower() not in allowed:
            raise ValueError(f'Environment must be one of: {allowed}')
        return v.lower()

    @field_validator('wildlens_footprint_multiclass_classifier_model_path')
    @classmethod
    def validate_multiclass_model_path(cls, v: Optional[str]) -> Optional[str]:
        if v and not pathlib.Path(v).exists():
            logger.warning(f"Multiclass classifier model path does not exist: {v}")
        return v

    @field_validator('wildlens_footprint_binary_classifier_model_path')
    @classmethod
    def validate_binary_model_path(cls, v: Optional[str]) -> Optional[str]:
        if v and not pathlib.Path(v).exists():
            logger.warning(f"Binary classifier model path does not exist: {v}")
        return v

    @field_validator('api_prefix')
    @classmethod
    def validate_api_prefix(cls, v: str) -> str:
        if not v.startswith('/'):
            v = f'/{v}'
        return v.rstrip('/')

    @model_validator(mode='after')
    def validate_production_requirements(self) -> 'Settings':
        if self.environment == 'production':
            if not self.wildlens_prediction_api_key:
                raise ValueError('WILDLENS_PREDICTION_API_KEY is required in production')
            if not self.wildlens_footprint_multiclass_classifier_model_path:
                raise ValueError('WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH is required in production')
            if not self.wildlens_footprint_binary_classifier_model_path:
                raise ValueError('WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH is required in production')
        return self

    def __post_init__(self):
        # Log model paths after initialization
        if self.wildlens_footprint_multiclass_classifier_model_path:
            logger.info(f"Multiclass Classifier model path: {self.wildlens_footprint_multiclass_classifier_model_path}")
        else:
            logger.warning("Multiclass Classifier model path not configured")

        if self.wildlens_footprint_binary_classifier_model_path:
            logger.info(f"Binary classifier model path: {self.wildlens_footprint_binary_classifier_model_path}")
        else:
            logger.warning("Binary classifier model path not configured")

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore"
    )


class DevelopmentSettings(Settings):
    environment: str = "development"
    debug: bool = True

    # Required values in development
    wildlens_prediction_api_key: str = Field(
        ...,
        description="Wildlens Prediction API key required in development"
    )
    wildlens_footprint_multiclass_classifier_model_path: str = Field(
        ...,
        description="Multiclass model path required in development"
    )
    wildlens_footprint_binary_classifier_model_path: str = Field(
        ...,
        description="Binary model path required in development"
    )


class ProductionSettings(Settings):
    environment: str = "production"
    debug: bool = False

    # Required values in production
    wildlens_prediction_api_key: str = Field(
        ...,
        description="Wildlens Prediction API key required in production"
    )
    wildlens_footprint_multiclass_classifier_model_path: str = Field(
        ...,
        description="Multiclass model path required in production"
    )
    wildlens_footprint_binary_classifier_model_path: str = Field(
        ...,
        description="Binary model path required in production"
    )


class TestingSettings(Settings):
    environment: str = "testing"
    debug: bool = True

    # Mock paths for testing
    wildlens_footprint_multiclass_classifier_model_path: Optional[str] = Field(
        default="tests/fixtures/mock_multiclass_model.keras",
        description="Mock multiclass model path for testing"
    )
    wildlens_footprint_binary_classifier_model_path: Optional[str] = Field(
        default="tests/fixtures/mock_binary_model.keras",
        description="Mock binary model path for testing"
    )


@lru_cache()
def create_settings() -> Settings:
    """
    Returns configuration based on environment.
    Uses cache to keep the config between each calls.
    """
    import os
    environment = os.getenv("ENVIRONMENT", "development").lower()

    settings = None
    if environment == "production":
        wildlens_prediction_api_key = os.getenv("WILDLENS_PREDICTION_API_KEY")
        multiclass_model_path = os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH")
        binary_model_path = os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH")

        settings = ProductionSettings(
            wildlens_prediction_api_key=wildlens_prediction_api_key,
            wildlens_footprint_multiclass_classifier_model_path=multiclass_model_path,
            wildlens_footprint_binary_classifier_model_path=binary_model_path
        )
    elif environment == "testing":
        settings = TestingSettings()
    else:
        wildlens_prediction_api_key = os.getenv("WILDLENS_PREDICTION_API_KEY")
        multiclass_model_path = os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH")
        binary_model_path = os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH")

        settings = DevelopmentSettings(
            wildlens_prediction_api_key=wildlens_prediction_api_key,
            wildlens_footprint_multiclass_classifier_model_path=multiclass_model_path,
            wildlens_footprint_binary_classifier_model_path=binary_model_path
        )

    settings.__post_init__()
    return settings


def get_settings() -> Settings:
    return create_settings()