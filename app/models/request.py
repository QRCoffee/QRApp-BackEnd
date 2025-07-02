from enum import Enum
from typing import List, Optional

from beanie import Link
from pydantic import Field

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
    staff: Optional["Link[User]"] = Field(default=None, description="Nhân viên xử lý yêu cầu") # type: ignore
    # ---- #
    service_unit: "Link[ServiceUnit]" = Field(..., description="Đơn vị phục vụ cụ thể, ví dụ: bàn số, quầy gọi món...") # type: ignore
    area: "Link[Area]" = Field(..., description="Khu vực thuộc chi nhánh, ví dụ: tầng, phòng, khu A...") # type: ignore
    branch: "Link[Branch]" = Field(..., description="Chi nhánh nơi phát sinh yêu cầu") # type: ignore
    business: "Link[Business]" = Field(..., description="Doanh nghiệp sở hữu chi nhánh và hệ thống phục vụ") # type: ignore
    # Ghi đè __action__ để thêm hành động 'share'
    __action__: List[str] = ["view","receive","delete","update"]



