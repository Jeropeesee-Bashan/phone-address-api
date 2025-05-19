from fastapi import FastAPI, Response

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from starlette.exceptions import HTTPException

from contextlib import asynccontextmanager

from .schema import PhoneAddressData, RussianPhoneNumber
from .config import *
from .keyval import KeyVal

from typing import Optional


storage: Optional[KeyVal] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global storage

    try:
        storage = await keyval_factory(settings)
        yield
    finally:
        if storage is not None:
            await storage.close()


app = FastAPI(
    title="phone-address-api",
    summary="API для работы с номерами телефонов и адресами.",
    description="""# Phone-Address API
Это **RESTful** сервис, позволяющий работать с данными каких-либо лиц
(номера телефонов, адреса): читать из и записывать в key-value базу данных.

Приложение разработано Андреем Куленко в рамках тестового задания для
AVE Technologies.

## Функциональность
Сервис предоставляет три обработчика по пути `/address`:
- **GET** - получить адрес по номеру телефона;
- **POST** - записать новый номер телефона вместе с адресом;
- **PUT** - обновить адрес по сохранённому номеру телефона;
- **DELETE** - удалить запись номера телефона и адреса.
""",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/address",
    response_model=PhoneAddressData,
    responses={
        HTTP_200_OK: {"description": "Адрес найден."},
        HTTP_404_NOT_FOUND: {"description": "Номер телефона не найден."},
    },
)
async def get_address(phone: RussianPhoneNumber):
    """Получение адреса по номеру телефона."""

    address = await storage.get(phone)
    if address is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Номер телефона не найден.")

    return PhoneAddressData(phone=phone, address=address)


@app.post(
    "/address",
    responses={
        HTTP_201_CREATED: {"description": "Номер телефона и адрес сохранены."},
        HTTP_400_BAD_REQUEST: {
            "description": "Адрес с таким номером телефона уже существует."
        },
    },
)
async def post_address(phone_address: PhoneAddressData, response: Response):
    """Запись нового номера телефона и адреса."""

    if await storage.contains(phone_address.phone):
        raise HTTPException(
            HTTP_400_BAD_REQUEST, "Адрес с таким номером телефона уже существует."
        )

    await storage.set(phone_address.phone, phone_address.address)
    response.status_code = HTTP_201_CREATED


# Хэндлер мог бы обрабатывать /address/{phone}, но тогда пришлось бы принимать
# один единственный параметр body, то есть прошлось бы написать ещё одну
# pydantic-модель для адреса. Оставим как есть - так лучше читается.
@app.put(
    "/address",
    responses={
        HTTP_200_OK: {"description": "Адрес обновлён."},
        HTTP_400_BAD_REQUEST: {"description": "Адрес не имеет изменений."},
        HTTP_404_NOT_FOUND: {
            "description": "Адреса с таким номером телефона не существует."
        },
    },
)
async def put_address(phone_address: PhoneAddressData, response: Response):
    """Обновление адреса по сохранённому номеру телефона."""

    address = await storage.get(phone_address.phone)
    if address is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND, "Адреса с таким номером телефона не существует."
        )

    if address == phone_address.address:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Адрес не имеет изменений.")

    await storage.set(phone_address.phone, phone_address.address)
    response.status_code = HTTP_200_OK


@app.delete(
    "/address",
    responses={
        HTTP_200_OK: {"description": "Номер телефона и адрес удалены."},
        HTTP_404_NOT_FOUND: {
            "description": "Адреса с таким номером телефона не существует."
        },
    },
)
async def delete_address(phone: RussianPhoneNumber, response: Response):
    """Удаление адреса по номеру телефона."""

    if not await storage.contains(phone):
        raise HTTPException(
            HTTP_404_NOT_FOUND, "Адреса с таким номером телефона не существует."
        )

    await storage.delete(phone)
    response.status_code = HTTP_200_OK
