from pydantic import field_validator
from sqlmodel import Field

from .base import Base


class User(Base, table=True):
    username:str = Field(nullable=False,unique=True)
    password:str = Field(nullable=False)
    email: str = Field(default=None,nullable=True,unique=True)
    role: str = Field(default="Staff",nullable=False)

    @field_validator("role")
    def validator(cls,v):
        allowed_roles = ["Staff", "Manager"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v
    
    class Config:
        orm_mode = True
        fields = {
            'password': {'exclude': True}
        }