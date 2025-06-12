from app.models import User
from app.schema.user import Auth, UserUpdate

from .base import Service


class UserService(Service[User, Auth, UserUpdate]):
    def __init__(self):
        super().__init__(User)

userService = UserService()

__all__ = ["userService"]