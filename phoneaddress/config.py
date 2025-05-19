from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, RedisDsn

from collections.abc import Callable
from .keyval import *


__all__ = ["settings", "keyval_factory"]


class Settings(BaseSettings):
    redis_url: RedisDsn = "redis://localhost:6379"
    host: str = "0.0.0.0"
    port: int = 80

    model_config = SettingsConfigDict(env_prefix="phoneaddress_")


settings = Settings()

keyval_factory: Callable[[Settings], KeyVal] = Redis
