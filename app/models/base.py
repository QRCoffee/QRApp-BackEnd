from pydantic import Field
from datetime import datetime
from typing import List, Optional
from beanie import (
    Document,
    Insert,
    PydanticObjectId,
    Replace,
    SaveChanges,
    Update,
    after_event, 
    before_event,
)

class Base(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Action Permissions
    __action__: List[str] = ["create", "view", "delete", "update"]

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @after_event([Replace, SaveChanges,Update,Insert])
    def set_updated_at(self):
        self.updated_at = datetime.now()

    def model_dump(self, *args, **kwargs) -> dict:
        kwargs.setdefault("by_alias", True)
        return super().model_dump(*args, **kwargs)
    
    @classmethod
    def get_actions(cls) -> List[str]:
        return cls.__action__