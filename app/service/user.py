from app.schema.user import UserCreate,UserUpdate
from app.models import User

from .base import Service


class UserService(Service[User, UserCreate, UserUpdate]):
    def __init__(self,db):
        super().__init__(User, db)

__all__ = ["UserService"]