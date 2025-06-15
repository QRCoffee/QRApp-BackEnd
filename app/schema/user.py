from typing import List, Literal, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, computed_field

from app.common.enum import PermissionCode, UserRole
from app.models import Permission
from app.schema import BaseResponse
from app.schema.permission import PermissionResponse
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
    permissions: List[int|Permission] = Field(default_factory=list)

class Staff(UserCreate):
    role: Literal[UserRole.STAFF] = Field(
        default=UserRole.STAFF,
        exclude=True,
    )

# class Staff(Auth):
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     address:Optional[str] = None

#     @computed_field(return_type=UserRole)
#     @property
#     def role(self) -> UserRole:
#         return UserRole.STAFF

#     @computed_field(return_type=List[int|Permission])
#     @property
#     def permissions(self):
#         return PermissionCode.get_permissions_by_role(self.role)
    
class Manager(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None

    @computed_field(return_type=UserRole)
    @property
    def role(self) -> UserRole:
        return UserRole.MANAGER

    @computed_field(return_type=List[int|Permission])
    @property
    def permissions(self):
        return PermissionCode.get_permissions_by_role(self.role)

class Administrator(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None

    @computed_field(return_type=UserRole)
    @property
    def role(self) -> UserRole:
        return UserRole.ADMIN

    @computed_field(return_type=List[int|Permission])
    @property
    def permissions(self):
        return PermissionCode.get_permissions_by_role(self.role)
    

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None

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

class UserDetailResponse(BaseResponse):
    username: str
    role: UserRole
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    permissions: List[PermissionResponse] = []
    restaurant: Optional[RestaurantResponse] = None