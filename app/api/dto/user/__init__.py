from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    role: Optional[str] = "Staff"


class UserUpdate(BaseModel):
    pass