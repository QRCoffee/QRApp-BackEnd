from app.models.business import BusinessType,Business
from app.schema.business import BusinessTypeCreate, BusinessTypeUpdate
from app.schema.business import BusinessCreate, BusinessUpdate
from app.service.base import Service


class BusinessTypeService(Service[BusinessType, BusinessTypeCreate, BusinessTypeUpdate]):
    def __init__(self):
        super().__init__(BusinessType)


class BusinessService(Service[Business, BusinessCreate, BusinessUpdate]):
    def __init__(self):
        super().__init__(Business)
businessTypeService = BusinessTypeService()
businessService = BusinessService()

__all__ = ["businessTypeService","businessService"]