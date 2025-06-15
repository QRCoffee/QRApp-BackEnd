from typing import Optional

from beanie import Insert, Link, before_event
from pydantic import Field

from app.common.exceptions import HTTP_409_CONFLICT
from app.models import Area

from .base import Base


class Table(Base):
    name: str = Field(...,nullable=False)
    area: Link[Area] = Field(...,nullable=False)
    capacity: int = Field(default=1,nullable=False,ge=0)
    image_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    @before_event(Insert)
    async def unique_table_in_area(self):
        from app.service import tableService
        tables = await tableService.find_many_by(conditions={
            "area._id":self.area.id
        })
        if any(table.name.lower() == self.name.lower() for table in tables):
            raise HTTP_409_CONFLICT(f"Bàn '{self.name}' đã tồn tại trong khu vực này")
