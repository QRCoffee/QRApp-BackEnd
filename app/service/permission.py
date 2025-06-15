from app.schema.permission import PermissionCreate, PermissionUpdate
from app.models.permission import Permission

from app.service.base import Service


class PermissionService(Service[Permission, PermissionCreate, PermissionUpdate]):
    def __init__(self):
        super().__init__(Permission)

permissionService = PermissionService()

__all__ = ["permissionService"]