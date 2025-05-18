from pydantic import BaseModel, Field

from pydantic_extra_types.phone_numbers import (
    PhoneNumber,
    PhoneNumberValidator,
)

from typing import Annotated


RussianPhoneNumber = Annotated[PhoneNumber, PhoneNumberValidator("RU", "E164")]


class PhoneAddressData(BaseModel):
    phone: RussianPhoneNumber = Field(
        examples=["+79991234567", "+7 900 111 11 11", "900 222 22 22"]
    )
    address: str
