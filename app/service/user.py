from beanie import Document

from app.models.user import User
from app.schema.user import Auth, UserUpdate
from app.service import permissionService

from .base import Service


class UserService(Service[User, Auth, UserUpdate]):
    def __init__(self):
        super().__init__(User)
    async def create(self, data):
        permissions = []
        for code in data.permissions:
            if p := await permissionService.find_one_by(
                by = "code",
                value = code,
            ):
                permissions.append(p)
        data = data.model_dump()
        data['permissions'] = permissions
        return await super().create(data)
    async def find_one_by(self, by = "_id", value = None):
        if by == "restaurant":
            by = "restaurant._id"
            if isinstance(value,Document):
                value = value.id
        return await super().find_one_by(by, value)
userService = UserService()

__all__ = ["userService"]