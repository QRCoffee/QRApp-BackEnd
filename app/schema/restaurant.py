from pydantic import BaseModel,Field
from typing import Optional,Union
from app.models import User,Restaurant
from beanie import PydanticObjectId

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