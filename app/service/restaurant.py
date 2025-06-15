from app.models.restaurant import Restaurant
from app.schema.restaurant import RestaurantCreate, RestaurantUpdate
from app.service.base import Service


class RestaurantService(Service[Restaurant, RestaurantCreate, RestaurantUpdate]):
    def __init__(self):
        super().__init__(Restaurant)

restaurantService = RestaurantService()

__all__ = ["restaurantService"]