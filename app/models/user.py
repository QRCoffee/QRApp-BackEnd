import bcrypt
from .base import Base
from sqlmodel import Field
class User(Base,table=True):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    email: str = Field(default=None,nullable=True,unique=True)
    phone: str = Field(default=None,nullable=True)

    def verify_password(self,password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))