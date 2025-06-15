from pydantic import BaseModel
from typing import Optional
from app.schema import BaseResponse

class TableCreate(BaseModel):
    name: str
    capacity: int
    image_url: Optional[str] = None

class TableUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[str] = None
    image_url: Optional[str] = None

class TableResponse(BaseResponse):
    name: str
    capacity: int
    image_url: Optional[str] = None
