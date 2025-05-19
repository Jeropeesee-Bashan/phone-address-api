from fastapi import FastAPI, Response

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from starlette.exceptions import HTTPException

from .schemas import PhoneAddressData, RussianPhoneNumber
from .config import *
from .keyval import KeyVal

from contextlib import asynccontextmanager


storage: KeyVal | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global storage

    try:
        storage = await keyval_factory(settings)
        yield
    finally:
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
- **PUT** - обновить адрес по существующему номеру телефона.
""",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/address", response_model=PhoneAddressData)
async def get_address(phone: RussianPhoneNumber):
    """Получение адреса по номеру телефона."""

    address = await storage[phone]
    if address is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Номер телефона не найден.")

    return PhoneAddressData(phone=phone, address=address)


@app.post("/address")
async def post_address(phone_address: PhoneAddressData, response: Response):
    """Запись нового номера телефона и адреса."""

    if await storage.__contains__(phone_address.phone):
        raise HTTPException(
            HTTP_400_BAD_REQUEST, "Адрес с таким номером телефона уже существует."
        )

    await storage.__setitem__(phone_address.phone, phone_address.address)
    response.status_code = HTTP_201_CREATED


@app.put("/address")
async def put_address(phone_address: PhoneAddressData, response: Response):
    """Обновление адреса по существующему номеру телефона."""

    if not await storage.__contains__(phone_address.phone):
        raise HTTPException(
            HTTP_400_BAD_REQUEST, "Адреса с таким номером телефона не существует."
        )

    await storage.__setitem__(phone_address.phone, phone_address.address)
    response.status_code = HTTP_200_OK
