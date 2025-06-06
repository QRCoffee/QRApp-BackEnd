from typing import Generic, TypeVar

from pydantic import BaseModel

Object = TypeVar("T")
class APIResponse(BaseModel,Generic[Object]):
    message: str
    data: Object