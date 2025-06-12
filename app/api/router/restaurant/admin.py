from fastapi import APIRouter, Depends
from app.common.enum import UserRole
from app.api.dependency import permissions
from app.common.responses import APIResponse
from app.common.exceptions import HTTP_404_NOT_FOUND,HTTP_409_CONFLICT
from app.schema.restaurant import RestaurantCreate,AssignRestaurant
from app.schema.user import UserResponse
from app.service import restaurantService,userService
AdminRouter = APIRouter(
    tags=["Restaurant: Admin"],
    prefix="/restaurants",
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ],
)

@AdminRouter.get(
    path = "", 
    name="List of restaurants"
)
async def get_restaurants():
    restaurants = await restaurantService.find_all()
    return APIResponse(
        data = restaurants
    )

@AdminRouter.post(
    path = "", 
    name="New Restaurants",
    response_model=APIResponse,
)
async def add_restaurants(data: RestaurantCreate):
    restaurant = await restaurantService.create(data)
    return APIResponse(
        data = restaurant
    )

@AdminRouter.post(
    path = "/assign",
    name = "Assign restaurant",
    response_model=APIResponse[UserResponse],
)
async def Assign_restaurant(data:AssignRestaurant):
    data = data.model_dump()
    restaurant_id = data.get("restaurant_id")
    owner_id = data.get("owner_id")
    restaurant = await restaurantService.find_by(value=restaurant_id)
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(f"Nhà hàng {restaurant_id} không tồn tại")
    owner = await userService.find_by(value=owner_id)
    if owner is None:
        raise HTTP_404_NOT_FOUND(f"Người dùng {owner_id} không tồn tại")
    holder = await userService.find_by(
        by="restaurant._id",
        value=restaurant.id,
    )
    if holder:
        raise HTTP_409_CONFLICT(
            message=f"Nhà hàng này được sở hữu bởi người dùng {holder.id}"
        )
    owner = await userService.update(
        id = owner_id,
        data = {
            "restaurant": restaurant
        }
    )
    return APIResponse(
        data = owner,
    )