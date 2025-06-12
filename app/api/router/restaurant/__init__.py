from fastapi import APIRouter,Depends
from app.schema.restaurant import RestaurantCreate
from app.common.exceptions import HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.models import Restaurant
from app.api.dependency import permissions
from app.common.enum import UserRole
from beanie import PydanticObjectId
from app.service import userService,restaurantService
apiRouter = APIRouter(
    tags=['Restaurant'],
    prefix="/restaurant",
)

@apiRouter.get(
    path="/{id}",
    name="Retrieve Restaurant",
    response_model=APIResponse[Restaurant],
)
async def retrieve(id: PydanticObjectId):
    restaurant = await restaurantService.find_by(value=id)
    if restaurant is None:
        raise HTTP_404_NOT_FOUND(
            message = "Không tìm thấy restaurant"
        )
    return APIResponse(
        data=restaurant,
    )

@apiRouter.post(
    path = "",
    response_model=APIResponse[Restaurant],
    response_model_exclude={
        "data": {"owner": {"password"}}
    }
)
async def create(data:RestaurantCreate, _ = Depends(permissions([UserRole.ADMIN]))):
    user = await userService.find_by(
        value = data.owner
    )
    if user is None:
        raise HTTP_404_NOT_FOUND(
            "Chủ sở hữu không tồn tại"
        )
    restaurant = await restaurantService.create(data)
    return APIResponse(
        data = restaurant
    )