import bcrypt

from app.models import User
from app.schema.user import UserCreate, UserUpdate

from .base import Service


class UserService(Service[User, UserCreate, UserUpdate]):
    def __init__(self,db):
        super().__init__(User, db)
    def create(self, data):
        salt = bcrypt.gensalt()
        if isinstance(data,dict):
            plain_password = data['password']
            data['password'] = bcrypt.hashpw(plain_password.encode(), salt).decode()
        else:
            plain_password = data.password
            data.password = bcrypt.hashpw(plain_password.encode(), salt).decode()
        return super().create(data)

__all__ = ["UserService"]