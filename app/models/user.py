import bcrypt
from beanie import Insert, before_event,Link
from pydantic import Field
from .base import Base
from app.common.enum import UserRole
from app.models.restaurant import Restaurant
class User(Base):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.STAFF)
    restaurant: Link[Restaurant] = Field(default=None)

    @before_event(Insert)
    def hash_password(self):
        if not self.password.startswith("$2b$"):
            self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self,password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))