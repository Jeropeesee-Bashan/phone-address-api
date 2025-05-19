from fastapi import FastAPI, Response

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
def get_address(phone: RussianPhoneNumber):
    """Получение адреса по номеру телефона"""
    pass


@app.post("/address")
def post_address(phone: PhoneAddressData, response: Response):
    """Запись нового номера телефона и адреса"""
    pass


@app.put("/address")
def put_address(phone: PhoneAddressData, response: Response):
    """Обновление адреса по существующему номеру телефона"""
    pass
