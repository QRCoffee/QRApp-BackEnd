from app.models.service_unit import ServiceUnit
from app.schema.service_unit import ServiceUnitCreate, ServiceUnitUpdate

from .base import Service


class ServiceUnitService(Service[ServiceUnit, ServiceUnitCreate, ServiceUnitUpdate]):
    def __init__(self):
        super().__init__(ServiceUnit)


unitService = ServiceUnitService()

__all__ = ["unitService"]
