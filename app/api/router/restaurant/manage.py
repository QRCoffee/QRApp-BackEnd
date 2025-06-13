from fastapi import APIRouter, Depends

from app.api.dependency import permissions
from app.common.enum import UserRole
from app.common.exceptions import HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.schema.restaurant import RestaurantResponse, RestaurantUpdate
from app.service import restaurantService

ManageRouter = APIRouter(
    tags = ["Manage: Restaurant"],
    prefix="/restaurant"
)
@ManageRouter.get(
    path = "",
    name  = "My Restaurant",
    status_code=200,
    response_model=APIResponse,
)
async def restaurant(payload = Depends(permissions([UserRole.MANAGER]))):
    restaurant = payload.pop("restaurant")
    if restaurant is None:
        restaurant = None
    return APIResponse(
        data=restaurant
    )

@ManageRouter.put(
    path = "",
    name  = "Update Restaurant",
    status_code=200,
    response_model=APIResponse[RestaurantResponse],
)
async def update_restaurant(data:RestaurantUpdate,payload = Depends(permissions([UserRole.MANAGER]))):
    restaurant = payload.pop("restaurant")
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(
            message="Bạn không sở hữu nhà hàng nào"
        )
    data = data.model_dump(exclude_none=True)
    restaurant = await restaurantService.update(
        id = restaurant.get("_id"),
        data = data,
    )
    return APIResponse(
        data=restaurant
    )