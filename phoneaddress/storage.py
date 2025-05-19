from fastapi import FastAPI
from contextlib import asynccontextmanager

from .config import *
from .keyval import KeyVal


storage: KeyVal | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global storage

    try:
        storage = await keyval_factory(settings)
        yield
    finally:
        await storage.close()
