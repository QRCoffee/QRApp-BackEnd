from enum import Enum
from typing import List

from beanie import Link
from pydantic import Field

from .base import Base


class OrderStatus(str, Enum):
    UNPAID = "Unpaid"
    PAID = "Paid"


class Order(Base):
    # General info
    items: List = Field(default_factory=list, description="Danh sách món")
    amount: float = Field(...)
    status: OrderStatus = Field(default=OrderStatus.UNPAID)
    # Business info
    business: "Link[Business]" = Field(...)  # type: ignore  # noqa: F821
    branch: "Link[Branch]" = Field(...)  # type: ignore  # noqa: F821
    area: "Link[Area]" = Field(...)  # type: ignore  # noqa: F821
    service_unit: "Link[ServiceUnit]" = Field(...)  # type: ignore  # noqa: F821
    staff: "Link[User]" = Field(...)  # type: ignore # noqa: F821
    request: "Link[Request]" = Field(...) # type: ignore # noqa: F821
