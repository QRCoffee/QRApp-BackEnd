from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query

from app.api.dependency import permissions
from app.common.enum import UserRole
from app.common.exceptions import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.user import UserResponse
from app.service import userService

AdminRouter = APIRouter(
    tags = ["Admin: User"]
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
async def get_users(
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50)
):
    skip = (page - 1) * limit
    users = await userService.find_all(
        skip=skip,
        limit=limit
    )
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
async def get_user(id: PydanticObjectId):
    user = await userService.find_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Người dùng {id} không tồn tại"
        )
    return APIResponse(
        data=user
    )

@AdminRouter.delete(
    path = "/users/{id}",
    name  = "Delete user",
    status_code=200,
    response_model=APIResponse,
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ]
)
async def delete_user(id: PydanticObjectId, payload = Depends(permissions([UserRole.ADMIN]))):
    user = await userService.find_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Người dùng {id} không tồn tại"
        )
    if str(user.id) == str(payload.get("_id")):
        raise HTTP_403_FORBIDDEN(
            message = "Hành động bị từ chối: bạn không thể tự xóa tài khoản của mình."
        )
    await userService.delete(id)
    return APIResponse(
        data = True
    )