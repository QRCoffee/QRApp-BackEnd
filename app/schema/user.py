from typing import Literal, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.common.enum import UserRole
from app.schema import BaseResponse
from app.schema.restaurant import RestaurantResponse


class Auth(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
class Session(BaseModel):
    refresh_token: str

class UserCreate(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    role: UserRole

class Staff(UserCreate):
    role: Literal[UserRole.STAFF] = Field(
        default=UserRole.STAFF,
        exclude=True,
    )

class Manager(UserCreate):
    role: Literal[UserRole.MANAGER] = Field(
        default=UserRole.MANAGER,
    )

class Administrator(UserCreate):
    role: Literal[UserRole.ADMIN] = Field(
        default=UserRole.ADMIN,
    )

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    restaurant: Optional[PydanticObjectId] = None

class UserResponse(BaseResponse):
    username: str
    role: UserRole
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    restaurant: Optional[RestaurantResponse] = None