from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / '.env',
        extra='ignore',
        hide_input_in_errors=True,
    )

    database_url: str
    secret_key: SecretStr
    access_token_expire_minutes: int = Field(default=30, gt=0)
    openai_api_key: SecretStr | None = None
    openai_model: str = 'gpt-4o-mini'
    openai_timeout_seconds: float = Field(default=30, gt=0, le=120)
    openai_max_retries: int = Field(default=2, ge=0, le=3)

    @field_validator('secret_key')
    @classmethod
    def require_secure_secret(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value()
        if len(secret.strip()) < 32 or secret in {
            'super_secret_key_needs_to_be_changed',
            'your_super_secret_key_change_this',
        }:
            raise ValueError('SECRET_KEY must be a unique secret of at least 32 characters')
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
