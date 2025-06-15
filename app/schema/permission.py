from app.schema import BaseResponse
from pydantic import BaseModel
from typing import Optional

class PermissionCreate(BaseModel):
    code: int
    description: str

class PermissionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None 

class PermissionResponse(BaseResponse):
    code: int
    description: str