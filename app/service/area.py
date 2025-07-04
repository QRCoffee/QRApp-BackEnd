from app.models.area import Area
from app.schema.area import AreaCreate, AreaUpdate
from app.service.base import Service


class AreaService(Service[Area, AreaCreate, AreaUpdate]):
    def __init__(self):
        super().__init__(Area)


areaService = AreaService()

__all__ = ["areaService"]
