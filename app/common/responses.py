from pydantic import BaseModel
from typing import TypeVar,Generic

Object = TypeVar("T")
class APIResponse(BaseModel,Generic[Object]):
    message: str
    data: Object