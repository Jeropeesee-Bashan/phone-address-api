from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
from typing import Annotated


class PhoneAddressData(BaseModel):
    phone: Annotated[PhoneNumber, PhoneNumberValidator("RU", "E164")]
    address: str
