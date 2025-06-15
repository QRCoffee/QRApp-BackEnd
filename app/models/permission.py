from .base import Base
from beanie import Indexed

class Permission(Base):
    code: int = Indexed(unique=True)
    description: str