from fastapi import APIRouter, Depends
from app.common.enum import UserRole
from app.api.dependency import permissions
from app.common.responses import APIResponse
from app.schema.restaurant import RestaurantCreate
from app.service import restaurantService,userService
ManageRouter = APIRouter(
    tags=["Restaurant: Manage"],
)

# @ManageRouter.post(
#     path = "/", 
#     name="New Restaurants",
#     response_model=APIResponse,
# )
# async def add_restaurants(data: RestaurantCreate,payload = Depends(permissions([UserRole.MANAGER]))):
#     owner = await userService.find_by(value=payload.get("_id"))
#     data = data.model_dump()
#     data['owner'] = owner
#     restaurant = await restaurantService.create(data)
#     return APIResponse(
#         data = restaurant
#     )