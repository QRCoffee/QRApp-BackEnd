from datetime import datetime

from beanie import Document, Insert, Replace, before_event,PydanticObjectId
from pydantic import Field,ConfigDict
from typing import Optional

class Base(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @before_event(Replace)
    def update_timestamp(self):
        self.updated_at = datetime.now()

    def model_dump(self, *args, **kwargs) -> dict:
        kwargs.setdefault("by_alias", True)
        return super().model_dump(*args, **kwargs)