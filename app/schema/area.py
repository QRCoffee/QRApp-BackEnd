from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.schema import BaseResponse


class AreaCreate(BaseModel):
    name: str
    branch: PydanticObjectId
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)

class AreaUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)

class AreaResponse(BaseResponse):
    name: str
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
