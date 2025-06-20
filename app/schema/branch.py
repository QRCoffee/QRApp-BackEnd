from typing import Optional

from pydantic import BaseModel

from app.models import Business
from app.schema import BaseResponse


class BranchCreateWithoutBusiness(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None
class BranchCreate(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None
    business: Business

class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None

class BranchResponse(BaseResponse):
    name: str
    address: str
    contact: Optional[str] = None