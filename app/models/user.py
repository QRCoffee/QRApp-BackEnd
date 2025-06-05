from .base import Base
from sqlmodel import Field
class User(Base,table=True):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    email: str = Field(default=None,nullable=True,unique=True)
    phone: str = Field(default=None,nullable=True)