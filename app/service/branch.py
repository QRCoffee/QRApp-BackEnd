from app.models.business import BusinessType
from app.schema.business import BusinessTypeCreate, BusinessTypeUpdate
from app.service.base import Service


class BusinessTypeService(Service[BusinessType, BusinessTypeCreate, BusinessTypeUpdate]):
    def __init__(self):
        super().__init__(BusinessType)

businessTypeService = BusinessTypeService()

__all__ = ["businessTypeService"]