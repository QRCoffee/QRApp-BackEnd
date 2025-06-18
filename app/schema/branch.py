from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

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