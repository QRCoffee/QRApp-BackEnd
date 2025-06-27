from typing import Optional

from beanie import Link
from pydantic import Field

from app.models import Business, Category, SubCategory

from .base import Base


class Product(Base):
    name: str = Field(...,description="Tên sản phẩm")
    description: Optional[str] = Field(default=None,description="Mô tả (Tùy chọn)")
    price: float = Field(...,description="Giá sản phẩm")
    # Refer - Hỗ trợ lọc
    category: Link[Category] 
    subcategory: Link[SubCategory]
    business: Link[Business]
