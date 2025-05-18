from .app import app
from .config import HOST, PORT

import uvicorn


__all__ = ["app", "main"]


def main() -> int:
    try:
        uvicorn.run(app=app, host=HOST, port=int(PORT))
    except:
        return 1

    return 0
