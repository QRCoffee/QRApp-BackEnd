from pydantic import BaseModel
from typing import Literal,Optional
from pydantic import Field
from app.common.enum import UserRole
from app.schema import BaseResponse

class Auth(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
class Session(BaseModel):
    refresh_token: str

class UserCreate(Auth):
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
    pass

class UserResponse(BaseResponse):
    username: str
    role: UserRole 