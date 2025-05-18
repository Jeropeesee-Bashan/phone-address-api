from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, RedisDsn


__all__ = ["settings"]


class Settings(BaseSettings):
    redis_url: RedisDsn = "redis://localhost:6379"
    host: str = "0.0.0.0"
    port: int = 80

    model_config = SettingsConfigDict(env_prefix="phoneaddress_")


settings = Settings()
