from fastapi import APIRouter, Depends

from app.api.dependency import permissions
from app.common.responses import APIResponse
from app.schema.user import ProfileUpdate, UserResponse
from app.service import userService

ManageRouter = APIRouter(
    tags = ["User: Self"],
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

@ManageRouter.put(
    path = "/me",
    name = "Update Profile",
    status_code=200,
    response_model=APIResponse[UserResponse],
)
async def update(data:ProfileUpdate,payload = Depends(permissions())):
    await userService.update(
        id = payload.get("_id"),
        data = data.model_dump(exclude_none=True)
    )
    user = await userService.find_by(value=payload.get("_id"))
    return APIResponse(
        data=user
    )