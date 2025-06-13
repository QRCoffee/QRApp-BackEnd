from beanie import Document

from app.models import User
from app.schema.user import Auth, UserUpdate

from .base import Service


class UserService(Service[User, Auth, UserUpdate]):
    def __init__(self):
        super().__init__(User)
    async def find_by(self, by = "_id", value = None):
        if by == "restaurant":
            by = "restaurant._id"
            if isinstance(value,Document):
                value = value.id
        return await super().find_by(by, value)
userService = UserService()

__all__ = ["userService"]