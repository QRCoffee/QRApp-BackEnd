from typing import Optional, Union

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models import Restaurant, User
from app.schema import BaseResponse


class RestaurantCreate(BaseModel):
    name: str = Field(..., description="Restaurant name")
    address: str = Field(..., description="Restaurant address")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class AssignRestaurant(BaseModel):
    restaurant_id: Union[PydanticObjectId,Restaurant]
    owner_id: Union[PydanticObjectId,User]

class RestaurantResponse(BaseResponse):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None