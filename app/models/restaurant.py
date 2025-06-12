from .base import Base
from typing import Optional
from pydantic import Field

class Restaurant(Base):
    name: str = Field(nullable=False)  
    address: str = Field(nullable=False)
    phone: Optional[str] = Field(default=None)