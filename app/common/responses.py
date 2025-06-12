from typing import Generic, TypeVar,Optional
from pydantic import BaseModel,ConfigDict
from app.common.enum import APIMessage
Object = TypeVar("T")
class APIResponse(BaseModel,Generic[Object]):
    model_config = ConfigDict(
        exclude_none=True  # ✅ Cấu hình chính thức để FastAPI áp dụng khi serialize
    )
    message: str = APIMessage.SUCCESS
    data: Optional[Object] = None