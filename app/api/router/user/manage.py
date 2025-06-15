from fastapi import APIRouter, Depends, Request

from app.api.dependency import required_role
from app.common.enum import UserRole
from app.common.responses import APIResponse
from app.schema.user import ProfileUpdate, UserDetailResponse
from app.service import userService

ManageRouter = APIRouter(
    tags = ["User: Self"],
)
@ManageRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse[UserDetailResponse],
)
async def profile(request: Request):
    user = await userService.find_one_by(value=request.state.user_id)
    return APIResponse(
        data=user
    )

@ManageRouter.put(
    path = "/me",
    name = "Update Profile",
    status_code=200,
    response_model=APIResponse[UserDetailResponse],
    dependencies = [
        Depends(required_role([
            UserRole.MANAGER,
            UserRole.ADMIN
        ]))
    ]
)
async def update(data:ProfileUpdate,request:Request):
    await userService.update(
        id = request.state.user_id,
        data = data.model_dump(exclude_none=True)
    )
    user = await userService.find_one_by(value=request.state.user_id)
    return APIResponse(
        data=user
    )