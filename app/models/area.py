from typing import Optional

from beanie import Link
from pydantic import Field

from .base import Base
from .restaurant import Restaurant


class Area(Base):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    restaurant: Link[Restaurant] = Field(nullable=False)
    is_active: bool = Field(default=True)