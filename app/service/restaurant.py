from app.models import Restaurant
from app.schema.restaurant import RestaurantCreate, RestaurantUpdate
from app.service import userService
from .base import Service
from pydantic import BaseModel

class RestaurantService(Service[Restaurant, RestaurantCreate, RestaurantUpdate]):
    def __init__(self):
        super().__init__(Restaurant)

restaurantService = RestaurantService()

__all__ = ["restaurantService"]