from typing import Optional,List

from beanie import PydanticObjectId
from pydantic import BaseModel
from app.models.product import Option
from app.schema import BaseResponse


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []
    sub_category: PydanticObjectId

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductResponse(BaseResponse):
    name: str
    description: Optional[str]
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []