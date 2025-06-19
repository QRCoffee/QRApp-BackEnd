from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from app.common.api_message import KeyResponse

Object = TypeVar("T")
class Response(BaseModel,Generic[Object]):
    model_config = ConfigDict(
        exclude_none=True
    )
    message: str = KeyResponse.SUCCESS
    data: Optional[Object] = None