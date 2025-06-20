from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.models import BusinessType, User
from app.schema import BaseResponse


class BusinessTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessTypeUpdate(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessTypeResponse(BaseResponse):
    name: str
    description: Optional[str] = None

class BusinessCreate(BaseModel):
    name: str
    address: str
    contact: str
    business_type: Link[BusinessType]
    tax_code: Optional[str] = None
    owner: Optional[Link[User]] = Field(description="Business Owner") # type: ignore

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    tax_code: Optional[str] = None

class FullBusinessResponse(BaseResponse):
    name: str 
    address: str
    contact: str
    tax_code: Optional[str] = None
    available: bool
    business_type: BusinessType
    owner: Optional[User] = Field(description="Business Owner") # type: ignore

class BusinessResponse(BaseResponse):
    name: str 
    address: str
    contact: str
    tax_code: Optional[str] = None
    available: bool
    business_type: BusinessType