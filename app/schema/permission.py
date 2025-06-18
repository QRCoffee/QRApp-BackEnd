from typing import Optional
from pydantic import BaseModel

from app.schema import BaseResponse


class PermissionCreate(BaseModel):
    code: str
    description: Optional[str] = None

class PermissionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None 

class PermissionResponse(BaseResponse):
    code: str
    description: Optional[str] = None