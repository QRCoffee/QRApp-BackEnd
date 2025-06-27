from datetime import datetime, timedelta
from typing import Optional

from beanie import Link
from pydantic import Field
from pymongo import IndexModel

from .base import Base


class BusinessType(Base):
    name: str = Field(..., description="Unique business type name")
    description: Optional[str] = Field(default=None, description="Optional description")

    class Settings:
        indexes = [
            IndexModel([("name", 1)], unique=True)
        ]


class Business(Base):
    name: str = Field(..., description="Tên doanh nghiệp (duy nhất)")
    address: str = Field(..., description="Địa chỉ doanh nghiệp (bao gồm: đường, thành phố, quốc gia, mã bưu điện)")
    contact: str = Field(..., description="Thông tin liên hệ (số điện thoại, email, website)")
    business_type: Link["BusinessType"] = Field(..., description="Loại hình doanh nghiệp")
    tax_code: Optional[str] = Field(default=None, description="Mã số thuế doanh nghiệp")
    owner: Optional["Link[User]"] = Field(default=None, description="Chủ sở hữu doanh nghiệp") # type: ignore
    available: bool = Field(default=True, description="Trạng thái hoạt động (True: đang hoạt động)")
    expired_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(minutes=1),
        description="Thời điểm hết hạn (mặc định là hiện tại + 15 phút)"
    )

    class Settings:
        indexes = [
            IndexModel([("name", 1)], unique=True)
        ]
    