from fastapi import APIRouter, Depends, Request

from app.api.dependency import require_restaurant, required_role
from app.api.router.area import apiRouter as AreaRouter
from app.common.enum import UserRole
from app.common.responses import APIResponse
from app.schema.restaurant import RestaurantResponse, RestaurantUpdate
from app.service import restaurantService

ManageRouter = APIRouter(
    tags = ["Manage: Restaurant"],
    prefix="/manage",
    dependencies= [
        Depends(required_role([UserRole.MANAGER])),
        Depends(require_restaurant)
    ]
)
@ManageRouter.get(
    path = "/restaurant",
    name  = "My Restaurant",
    status_code=200,
    response_model=APIResponse[RestaurantResponse],
)
async def restaurant(request:Request):
    restaurant = await restaurantService.find_one_by(
        by="_id",
        value=request.state.restaurant_id,
    )
    return APIResponse(data=restaurant)

@ManageRouter.put(
    path = "/restaurant",
    name  = "Update Restaurant",
    status_code=200,
    response_model=APIResponse[RestaurantResponse],
)
async def update_restaurant(data:RestaurantUpdate,request: Request):
    data = data.model_dump(exclude_none=True)
    restaurant = await restaurantService.update(
        id = request.state.restaurant_id,
        data = data,
    )
    return APIResponse(
        data=restaurant
    )

ManageRouter.include_router(AreaRouter)