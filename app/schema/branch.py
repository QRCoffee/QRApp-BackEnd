from typing import Optional
from pydantic import BaseModel
from app.schema import BaseResponse
from app.models import Business


class BranchCreate(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None
    business: Business

class BranchUpdate(BaseModel):
    name: str
    address: str
    contact: Optional[str] = None

class BranchResponse(BaseResponse):
    name: str
    address: str
    contact: Optional[str] = None