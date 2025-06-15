from beanie import Indexed

from .base import Base


class Permission(Base):
    code: int = Indexed(unique=True)
    description: str