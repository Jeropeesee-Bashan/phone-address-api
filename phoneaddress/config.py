import os

from uvicorn import Config


__all__ = ["REDIS_URL", "HOST", "PORT", "server_config"]

REDIS_URL = os.getenv("PHONEADDRESS_REDIS_URL", "redis://localhost:6379")
HOST = os.getenv("PHONEADDRESS_HOST", "0.0.0.0")
PORT = os.getenv("PHONEADDRESS_PORT", "80")
