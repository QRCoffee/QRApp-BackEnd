from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query

from app.api.dependency import required_role
from app.common.enum import UserRole
from app.common.exceptions import (HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_409_CONFLICT)
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.restaurant import (AssignRestaurant, RestaurantCreate,
                                   RestaurantResponse)
from app.schema.user import UserDetailResponse, UserUpdate
from app.service import restaurantService, userService

AdminRouter = APIRouter(
    tags=["Admin: Restaurant"],
    prefix="/restaurants",
    dependencies=[
        Depends(required_role([UserRole.ADMIN]))
    ],
)

@AdminRouter.get(
    path = "", 
    name="List of restaurants",
    response_model=APIResponse[List[RestaurantResponse]]
)
async def get_restaurants(
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50),
    name: str = Query(default=None),
    address: str = Query(default=None),
):
    conditions = {}
    if name:
        conditions['name'] = {
            "$regex": name,
            "$options": "i"
        }
    if address:
        conditions['address'] = {
            "$regex": address,
            "$options": "i"
        }
    restaurants = await restaurantService.find_many_by(
        conditions,
        skip=(page - 1) * limit,
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
    restaurants = await restaurantService.find_one_by(
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
    response_model=APIResponse[UserDetailResponse],
)
async def Assign_restaurant(data:AssignRestaurant):
    data = data.model_dump()
    restaurant_id = data.get("restaurant_id")
    owner_id = data.get("owner_id")
    # 1. Check restaurant
    restaurant = await restaurantService.find_one_by(value=restaurant_id)
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(f"Nhà hàng {restaurant_id} không tồn tại")
    # 2. Check owner
    owner = await userService.find_one_by(value=owner_id)
    if owner is None:
        raise HTTP_404_NOT_FOUND(f"Người dùng {owner_id} không tồn tại")
    # 3. Check role
    if owner.role != UserRole.MANAGER:
        raise HTTP_403_FORBIDDEN("Yêu cầu 'Manager' để sở hữu nhà hàng")
    holder = await userService.find_one_by(
        by="restaurant",
        value=restaurant,
    )
    if holder:
        raise HTTP_409_CONFLICT(
            message=f"Nhà hàng này được sở hữu bởi người dùng {holder.id}"
        )
    owner = await userService.update(
        id = owner_id,
        data = {
            "restaurant":restaurant
        }
    )
    await owner.fetch_all_links()
    return APIResponse(
        data = owner,
    )

@AdminRouter.delete(
    path = "/{id}",
    name = "Delete restaurant",
    response_model=APIResponse[RestaurantResponse]

)
async def delete_restaurant(id:PydanticObjectId):
    restaurant = await restaurantService.find_one_by(value=id)
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Nhà hàng {id} không tồn tại"
        )
    owner = await userService.find_one_by(
        by="restaurant",
        value=restaurant,
    )
    if owner:
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