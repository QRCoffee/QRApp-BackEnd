from typing import Optional

from beanie import Insert, before_event
from pydantic import Field

from app.common.enum import APIMessage
from app.common.exceptions import HTTP_409_CONFLICT

from .base import Base


class Restaurant(Base):
    name: str = Field(nullable=False)  
    address: str = Field(nullable=False)
    phone: Optional[str] = Field(default=None)

    @before_event(Insert)
    async def unique_phone_number(self):
        from app.service import restaurantService
        if self.phone is not None:
            holder = await restaurantService.find_by(
                by = "phone",
                value = self.phone
            )
            if holder:
                raise HTTP_409_CONFLICT(APIMessage.PHONE_CONFLIC)