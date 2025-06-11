import bcrypt
from beanie import Insert, before_event
from pydantic import Field
from enum import Enum
from .base import Base


class UserRole(str, Enum):
    MANAGER = "Manager"
    STAFF = "Staff"

class User(Base):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.STAFF)
    @before_event(Insert)
    def hash_password(self):
        if not self.password.startswith("$2b$"):
            self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self,password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    