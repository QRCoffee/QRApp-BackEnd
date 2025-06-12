from app.models import Restaurant
from app.schema.restaurant import RestaurantCreate, RestaurantUpdate
from app.service import userService
from .base import Service


class RestaurantService(Service[Restaurant, RestaurantCreate, RestaurantUpdate]):
    def __init__(self):
        super().__init__(Restaurant)

    async def create(self, data):
        user = await userService.find_by(value=data.owner)
        data.owner = user
        return await super().create(data)
restaurantService = RestaurantService()

__all__ = ["restaurantService"]