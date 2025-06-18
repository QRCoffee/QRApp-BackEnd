from typing import Optional

from pydantic import BaseModel, Field


class AreaCreate(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)

class AreaUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
