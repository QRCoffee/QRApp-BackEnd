import bcrypt
from sqlmodel import Field

from .base import Base


class User(Base,table=True):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    phone: str = Field(default=None,nullable=True)

    def verify_password(self,password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))