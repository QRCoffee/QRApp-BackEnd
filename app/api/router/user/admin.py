from fastapi import APIRouter,Depends
from beanie import PydanticObjectId
from app.common.responses import APIResponse
from typing import List
from app.common.enum import UserRole
from app.common.exceptions import HTTP_404_NOT_FOUND
from app.schema.user import UserResponse
from app.api.dependency import permissions
from app.service import userService
AdminRouter = APIRouter(
    tags = ["User: Admin"]
)
@AdminRouter.get(
    path = "/users",
    name  = "List of users",
    status_code=200,
    response_model=APIResponse[List[UserResponse]],
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ]
)
async def get_users():
    users = await userService.find_all()
    return APIResponse(
        data=users
    )

@AdminRouter.get(
    path = "/users/{id}",
    name  = "Detail user",
    status_code=200,
    response_model=APIResponse[UserResponse],
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ]
)
async def get_users(id: PydanticObjectId):
    user = await userService.find_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Người dùng {id} không tồn tại"
        )
    return APIResponse(
        data=user
    )