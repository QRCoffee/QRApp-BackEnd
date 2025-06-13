from typing import Optional

from beanie import Link
from pydantic import Field

from app.models import Area

from .base import Base


class Table(Base):
    name: str = Field(...,nullable=False)
    description: Optional[str] = Field(...,default=None)
    area: Link[Area] = Field(...,nullable=False)
    qr_code: str = Field(default=None,nullable=True)
    is_active: bool = Field(default=True)