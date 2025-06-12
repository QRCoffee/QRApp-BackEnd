from pydantic import BaseModel, Field, field_validator,ConfigDict
from datetime import datetime
from bson import ObjectId


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes=True,
    )
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v