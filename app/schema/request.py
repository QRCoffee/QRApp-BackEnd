from typing import List, Optional

from beanie import Link, PydanticObjectId
from pydantic import BaseModel, Field
from app.schema.area import AreaResponse
from app.schema.service_unit import ServiceUnitResponse
from app.models.request import RequestStatus, RequestType
from app.models.user import User
from app.schema import BaseResponse


class RequestCreate(BaseModel):
    type: RequestType = Field(..., description="Loại yêu cầu (Order / Checkout)")
    reason: Optional[str] = Field(default=None, description="Lý do yêu cầu")
    service_unit: PydanticObjectId
    guest_name: Optional[str] = Field(default=None)
    area: PydanticObjectId
    data: List = []


class RequestUpdate(BaseModel):
    status: Optional[RequestStatus] = RequestStatus.COMPLETE
    staff: Optional[Link[User]] = None


class ResquestResponse(BaseResponse):
    type: RequestType
    reason: Optional[str] = None
    status: RequestStatus
    guest_name: Optional[str] = None
    area: AreaResponse
    service_unit: ServiceUnitResponse
    data: List = []
