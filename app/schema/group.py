from typing import Optional,List
from app.schema import BaseResponse
from pydantic import BaseModel, Field
from app.schema.permission import DetailPermissionResponse

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, description="Optional description")

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupResponse(BaseResponse):
    name: str
    description: Optional[str] = None
    permissions: List[DetailPermissionResponse] = []