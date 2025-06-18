from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import Optional
from app.schema import BaseResponse

class BranchCreate(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None
    business: PydanticObjectId

class BranchUpdate(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None

class BranchResponse(BaseResponse):
    name: str
    address: str
    contact: Optional[str] = None