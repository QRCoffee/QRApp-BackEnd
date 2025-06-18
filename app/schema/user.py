from pydantic import BaseModel, Field, computed_field
from typing import Optional,Literal,List
from beanie import Link,PydanticObjectId
from app.models import Permission,Group,Business

class Auth(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
class Session(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    image_url: Optional[str] = None
    role: Literal['Admin','BusinessOwner','Staff'] = 'Staff'
    permissions: List[Link[Permission]] = Field(
        default_factory=list,
    )
    group: Link[Group] = None
    scope: Optional[Link[Business]] = None
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    image_url: Optional[str] = None

class Administrator(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    
    @computed_field(return_type=str)
    @property
    def role(self) -> str:
        return "Admin"

class BusinessOwner(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    
    @computed_field(return_type=str)
    @property
    def role(self) -> str:
        return "BusinessOwner"
    
class Staff(Auth):
    name: Optional[str] = None
    phone: Optional[str] = None
    address:Optional[str] = None
    
    @computed_field(return_type=str)
    @property
    def role(self) -> str:
        return "Staff"
class BusinessRegister(Auth):
    # owner
    owner_name: str
    owner_address: str
    owner_contact: str
    # business
    business_name: str
    business_address: str
    business_contact: str
    business_type: PydanticObjectId
    business_tax_code: Optional[str] = Field(default=None, description="Business tax code")

    @computed_field(return_type=str)
    @property
    def role(self) -> str:
        return "BusinessOwner"
