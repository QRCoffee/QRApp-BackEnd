from .base import Base
from typing import Optional
from .user import User
from pydantic import Field
from beanie import Link

class Restaurant(Base):
    name: str = Field(nullable=False)  
    address: str = Field(nullable=False)
    phone: Optional[str] = Field(default=None)
    owner: Link[User] = Field(nullable=False)
