from typing import Any, Dict, List, Optional

from beanie import Link
from pydantic import Field

from app.models import Business, Category, SubCategory

from .base import Base


class Product(Base):
    name: str = Field(...,description="Tên sản phẩm")
    description: Optional[str] = Field(default=None,description="Mô tả (Tùy chọn)")
    price: float = Field(...,description="Giá sản phẩm")
    variants: List[Dict[str,Any]] = Field(default_factory=list,description="Các biến thể của sản phẩm")
    options: List[Dict[str,Any]] = Field(default_factory=list,description="Các option đi kèm của sản phẩm")
    img_url: Optional[str] = Field(default=None,description="Ảnh mô tả")
    # Refer - Hỗ trợ lọc
    category: Link[Category] 
    subcategory: Link[SubCategory]
    business: Link[Business]
