from datetime import datetime

from beanie import Document, Insert, Replace, before_event
from pydantic import Field


class Base(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @before_event(Replace)
    def update_timestamp(self):
        self.updated_at = datetime.now()