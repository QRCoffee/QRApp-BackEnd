from typing import Optional

from beanie import Link
from pydantic import Field

from app.models.base import Base
from app.models.business import Business
from app.models.branch import Branch


class Area(Base):
    name: str = Field(..., description="Tên khu vực trong doanh nghiệp (ví dụ: Tầng 1, Khu A, Quầy tiếp tân...)")
    description: Optional[str] = Field(None, description="Mô tả thêm về khu vực")
    image_url: Optional[str] = Field(None, description="Đường dẫn ảnh minh họa khu vực (nếu có)")
    branch: Link[Branch] = Field(..., description="Chi nhánh sở hữu")
    business: Link[Business] = Field(..., description="Doanh nghiệp sở hữu khu vực này")
