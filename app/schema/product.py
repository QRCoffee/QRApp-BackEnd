from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.models.product import Option
from app.schema import BaseResponse
from app.schema.category import CategoryResponse, SubCategoryResponse


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []
    sub_category: PydanticObjectId


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []


class ProductResponse(BaseResponse):
    name: str
    description: Optional[str]
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []
    img_url: Optional[str] = None


class FullProductResponse(BaseResponse):
    name: str
    description: Optional[str]
    variants: Optional[List[Option]] = []
    options: Optional[List[Option]] = []
    subcategory: SubCategoryResponse
    category: CategoryResponse
    img_url: Optional[str] = None
    # business: BusinessResponse
