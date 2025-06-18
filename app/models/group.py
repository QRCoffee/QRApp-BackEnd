from pydantic import Field
from .base import Base
from beanie import Link
from typing import Optional,List
from app.models.permission import Permission
from app.models.business import Business

class Group(Base):
    name: str
    description: Optional[str] = Field(default=None, description="Optional description")
    scope: Optional[Link[Business]] = Field(default=None)
    permissions: List[Link[Permission]] = Field(
        default_factory=list,
    )