from .base import Base
from beanie import Link
from typing import Optional
from pydantic import Field
from app.models import Restaurant
class Area(Base):
    name: str = Field(...,nullable=False)
    description: Optional[str] = Field(default=None)
    restaurant: Link[Restaurant] = Field(nullable=False)
    is_active: bool = Field(default=True)