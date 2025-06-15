from typing import Optional

from pydantic import BaseModel

from app.schema import BaseResponse
from app.schema.restaurant import RestaurantResponse


class AreaCreate(BaseModel):
    name: str
    description: Optional[str] = None 
    image_url: Optional[str] = None
class AreaUpdate(BaseModel):
    name: str
    description: Optional[str] = None 
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class AreaResponse(BaseResponse):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    restaurant: RestaurantResponse 
    is_active: bool