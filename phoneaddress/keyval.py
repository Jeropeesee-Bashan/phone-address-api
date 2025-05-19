from abc import ABC, abstractmethod
from collections.abc import Callable, Awaitable

import redis.asyncio as redis


__all__ = ["KeyVal", "Redis"]


class KeyVal(ABC):
    """Интерфейс, абстрагирующий key-val хранилища."""

    @abstractmethod
    async def __new__(cls, settings: "Settings") -> "KeyVal":
        """Фабрика экземпляров подключения к key-val хранилищу."""
        return super().__new__(cls)

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Получить значение из key-val хранилища."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str):
        """Записать значение в key-val хранилище."""
        pass

    async def contains(self, key: str) -> bool:
        """Проверить наличие ключа в key-val хранилище."""
        pass

    @abstractmethod
    async def close(self):
        """Закрыть подключение к key-val хранилищу."""
        pass


class Redis(KeyVal):
    """Key-val хранилище Redis."""

    async def __new__(cls, settings: "Settings") -> KeyVal:
        result = await super().__new__(cls, settings)

        client = await redis.from_url(str(settings.redis_url))
        await client.ping()
        cls.__init__(result, client)

        return result

    def __init__(self, client: redis.client):
        self._client = client

    async def get(self, key: str) -> str | None:
        r = await self._client.get(key)
        if r is not None and isinstance(r, bytes):
            r = r.decode()

        return r

    async def set(self, key: str, value: str):
        await self._client.set(key, value)

    async def contains(self, key: str) -> bool:
        return await self._client.exists(key)

    async def close(self):
        await self._client.close()
