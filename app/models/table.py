from .base import Base
from beanie import Link
from typing import Optional
from pydantic import Field
from app.models import Area

class Table(Base):
    name: str = Field(...,nullable=False)
    description: Optional[str] = Field(...,default=None)
    area: Link[Area] = Field(...,nullable=False)
    qr_code: str = Field(default=None,nullable=True)
    is_active: bool = Field(default=True)