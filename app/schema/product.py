from typing import Any, Dict, List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schema import BaseResponse


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    variants: Optional[List[Dict[str,Any]]] = []
    options: Optional[List[Dict[str,Any]]] = []
    sub_category: PydanticObjectId

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductResponse(BaseResponse):
    name: str
    description: Optional[str]
    price: float
    variants: Optional[List[Dict[str,Any]]] = []
    options: Optional[List[Dict[str,Any]]] = []