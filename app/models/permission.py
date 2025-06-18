from pydantic import Field
from typing import Optional,List
from .base import Base
from pymongo import IndexModel

class Permission(Base):
    code: str = Field(..., description="Unique permission code")
    description: Optional[str] = Field(default=None, description="Optional description")

    # Ghi đè __action__ để thêm hành động 'share'
    __action__: List[str] = ["view","share"]

    class Settings:
        indexes = [
            IndexModel([("code", 1)], unique=True)
        ]