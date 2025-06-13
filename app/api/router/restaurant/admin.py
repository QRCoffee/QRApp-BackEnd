from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query

from app.api.dependency import permissions
from app.common.enum import UserRole
from app.common.exceptions import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_409_CONFLICT)
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.restaurant import (AssignRestaurant, RestaurantCreate,
                                   RestaurantResponse)
from app.schema.user import UserResponse, UserUpdate
from app.service import restaurantService, userService

AdminRouter = APIRouter(
    tags=["Restaurant: Admin"],
    prefix="/restaurants",
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ],
)

@AdminRouter.get(
    path = "", 
    name="List of restaurants",
    response_model=APIResponse[List[RestaurantResponse]]
)
async def get_restaurants(
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50)
):
    skip = (page - 1) * limit
    restaurants = await restaurantService.find_all(
        skip=skip,
        limit=limit
    )
    return APIResponse(
        data = restaurants
    )

@AdminRouter.get(
    path = "/{id}", 
    name="Detail restaurants",
    response_model=APIResponse[RestaurantResponse]
)
async def get_restaurant(id: PydanticObjectId):
    restaurants = await restaurantService.find_by(
        value=id,
    )
    if restaurants is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Nhà hàng {id} không tồn tại"
        )
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
        by="restaurant",
        value=restaurant,
    )
    if holder:
        raise HTTP_409_CONFLICT(
            message=f"Nhà hàng này được sở hữu bởi người dùng {holder.id}"
        )
    owner = await userService.update(
        id = owner_id,
        data = UserUpdate(
            restaurant=restaurant
        )
    )
    return APIResponse(
        data = owner,
    )

@AdminRouter.delete(
    path = "/{id}",
    name = "Delete restaurant",
    response_model=APIResponse[RestaurantResponse]

)
async def delete_restaurant(id:PydanticObjectId):
    restaurant = await restaurantService.find_by(value=id)
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Nhà hàng {id} không tồn tại"
        )
    owner = await userService.find_by(
        by="restaurant",
        value=restaurant,
    )
    if owner is None:
        raise HTTP_400_BAD_REQUEST(message="Chủ sở hữu không khả thi")
    await userService.update(
        id = owner.id,
        data = UserUpdate(
            restaurant=None
        )
    )
    await restaurantService.delete(id)
    return APIResponse(
        data=restaurant
    )