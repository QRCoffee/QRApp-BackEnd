from app.models import User
from app.schema.user import UserCreate, UserUpdate

from .base import Service


class UserService(Service[User, UserCreate, UserUpdate]):
    pass

__all__ = ["UserService"]