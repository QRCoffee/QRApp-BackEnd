from app.models import Area
from app.schema.area import AreaCreate, AreaUpdate

from .base import Service


class AreaService(Service[Area, AreaCreate, AreaUpdate]):
    def __init__(self):
        super().__init__(Area)

areaService = AreaService()

__all__ = ["areaService"]