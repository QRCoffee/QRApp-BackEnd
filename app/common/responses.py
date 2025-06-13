from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from app.common.enum import APIMessage

Object = TypeVar("T")
class APIResponse(BaseModel,Generic[Object]):
    model_config = ConfigDict(
        exclude_none=True
    )
    message: str = APIMessage.SUCCESS
    data: Optional[Object] = None