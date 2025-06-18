from pydantic import BaseModel,Field
from typing import Optional

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, description="Optional description")

class GroupUpdate(BaseModel):
    pass