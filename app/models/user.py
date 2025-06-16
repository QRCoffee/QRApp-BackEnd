from typing import List, Optional

import bcrypt
from beanie import Insert, Link, Update, before_event
from pydantic import Field

from app.common.enum import APIMessage, UserRole
from app.common.exceptions import HTTP_409_CONFLICT
from app.models.permission import Permission
from app.models.restaurant import Restaurant

from .base import Base


class User(Base):
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    name: Optional[str] = Field(default=None,nullalbe=True)
    phone: Optional[str] = Field(default=None,nullalbe=True)
    address:Optional[str] = Field(default=None,nullalbe=True)
    restaurant: Optional[Link[Restaurant]] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    role: UserRole = Field(default=UserRole.STAFF)
    permissions: List[Link[Permission]] = Field(
        default_factory=list,
    )

    @before_event(Insert)
    def hash_password(self):
        if not self.password.startswith("$2b$"):
            self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @before_event([Insert,Update])
    async def unique_username(self):
        from app.service import userService
        user = await userService.find_one_by(by="username", value=self.username)
        if user and self.id != user.id:
            raise HTTP_409_CONFLICT(APIMessage.USERNAME_CONFLIC)
    
    @before_event([Insert,Update])
    async def unique_phone_number(self):
        from app.service import userService
        if self.phone is not None:
            holder = await userService.find_one_by(
                by = "phone",
                value = self.phone
            )
            if holder and holder.id != self.id:
                raise HTTP_409_CONFLICT(APIMessage.PHONE_CONFLIC)


    def verify_password(self,password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))