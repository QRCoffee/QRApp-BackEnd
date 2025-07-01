from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models.request import RequestType


class RequestCreate(BaseModel):
    type: RequestType = Field(..., description="Loại yêu cầu (Order / Checkout)")
    reason: Optional[str] = Field(default=None, description="Lý do yêu cầu")
    service_unit: PydanticObjectId
    area: PydanticObjectId