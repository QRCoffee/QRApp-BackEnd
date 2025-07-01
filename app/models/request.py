from enum import Enum
from typing import Optional

from beanie import Link
from pydantic import Field

from app.models import Area, Branch, Business, ServiceUnit, User
from app.models.base import Base


class RequestType(str, Enum):
    ORDER = "Order"
    CHECKOUT = "Checkout"

class RequestStatus(str, Enum):
    CANCELLED = "Cancelled"
    PENDING = "Pending"
    COMPLETE = "Complete"

class Request(Base):
    type: RequestType = Field(..., description="Loại yêu cầu (Order / Checkout)")
    reason: Optional[str] = Field(default=None, description="Lý do yêu cầu")
    status: RequestStatus = Field(default=RequestStatus.PENDING, description="Trạng thái xử lý")
    staff: Optional[Link[User]] = Field(default=None, description="Nhân viên xử lý yêu cầu")
    # ---- #
    service_unit: Link[ServiceUnit] = Field(..., description="Đơn vị phục vụ cụ thể, ví dụ: bàn số, quầy gọi món...")
    area: Link[Area] = Field(..., description="Khu vực thuộc chi nhánh, ví dụ: tầng, phòng, khu A...")
    branch: Link[Branch] = Field(..., description="Chi nhánh nơi phát sinh yêu cầu")
    business: Link[Business] = Field(..., description="Doanh nghiệp sở hữu chi nhánh và hệ thống phục vụ")



