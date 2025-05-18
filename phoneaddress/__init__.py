from .app import app
from .config import settings

import uvicorn


__all__ = ["app", "main"]


def main() -> int:
    try:
        uvicorn.run(app=app, host=settings.host, port=settings.port)
    except:
        return 1

    return 0
