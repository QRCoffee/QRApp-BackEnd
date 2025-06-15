from typing import Optional

from beanie import Insert, Link, before_event
from pydantic import Field

from app.common.exceptions import HTTP_409_CONFLICT

from .base import Base
from .restaurant import Restaurant


class Area(Base):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    restaurant: Link[Restaurant] = Field(nullable=False)
    image_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    @before_event(Insert)
    async def unique_name_in_areas(self):
        from app.service import areaService
        areas = await areaService.find_many_by(
            conditions={
                "restaurant._id": self.restaurant.id,
            }
        )
        if any(area.name.lower() == self.name.lower() for area in areas):
            raise HTTP_409_CONFLICT(f"Khu vực '{self.name}' đã tồn tại trong nhà hàng này")