import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Base(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())