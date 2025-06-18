from pydantic import BaseModel,field_validator,Field
from beanie import Link
from app.models import BusinessType,User
from typing import Optional
from app.schema import BaseResponse


class BusinessTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    def uppercase_name(cls, v: str) -> str:
        return v.upper()

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

class BusinessResponse(BaseResponse):
    name: str 
    address: str
    contact: str
    business_type: BusinessType
    tax_code: Optional[str] = None
    owner: Optional[User] = Field(description="Business Owner") # type: ignore