from typing import Optional

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, description="Optional description")

class GroupUpdate(BaseModel):
    pass