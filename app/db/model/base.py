from datetime import datetime

from sqlmodel import Field, SQLModel


def generate_id() -> str:
    import uuid
    return str(uuid.uuid4())
class Base(SQLModel):
    id: str = Field(default_factory=generate_id, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
