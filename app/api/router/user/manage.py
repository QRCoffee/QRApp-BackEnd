from fastapi import APIRouter, Depends

from app.api.dependency import permissions
from app.common.responses import APIResponse
from app.schema.user import UserResponse

ManageRouter = APIRouter(
    tags = ["User: Manage"],
)
@ManageRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse[UserResponse],
)
async def profile(payload = Depends(permissions())):
    payload.pop("restaurant")
    return APIResponse(
        data=payload
    )

@ManageRouter.get(
    path = "/restaurant",
    name  = "My Restaurant",
    status_code=200,
    response_model=APIResponse,
)
async def restaurant(payload = Depends(permissions())):
    restaurant = payload.pop("restaurant")
    if restaurant.get("id") == 'None':
        restaurant = None
    return APIResponse(
        data=restaurant
    )

@ManageRouter.put(
    path = "/me",
    name = "Update Profile",
    status_code=200,
    # response_model=APIResponse,
)
async def update(payload = Depends(permissions())):
    return payload