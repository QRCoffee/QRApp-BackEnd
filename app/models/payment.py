from typing import Optional

from beanie import Link
from pydantic import Field

from app.models import User

from .base import Base


class Payment(Base):
    owner: Link[User] = Field(...,"Chủ sở hữu")
    bank_name: str = Field(..., description="Tên ngân hàng, ví dụ: Vietcombank")
    bank_code: Optional[str] = Field(None, description="Mã ngân hàng, ví dụ: VCB")
    account_name: str = Field(..., description="Tên chủ tài khoản")
    account_number: str = Field(..., description="Số tài khoản ngân hàng")
    branch: Optional[str] = Field(None, description="Chi nhánh ngân hàng")
    country: Optional[str] = Field("VN", description="Quốc gia, mặc định là Việt Nam")    
