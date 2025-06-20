from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.user import User
from app.schema import BaseResponse
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

class FullGroupResponse(GroupResponse):
    users: Optional[List[User]] = []

    @classmethod
    async def from_model(cls, model: GroupResponse) -> "FullGroupResponse":
        data = model.model_dump()
        from app.service import userService
        users = await userService.find_many({})
        return cls(**data,users=users)