from pydantic import BaseModel
from app.common.enum import UserRole
from app.schema import BaseResponse
class UserCreate(BaseModel):
    pass
class UserUpdate(BaseModel):
    pass

class UserResponse(BaseResponse):
    username: str
    role: UserRole 