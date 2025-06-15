from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query, Request

from app.api.dependency import required_role
from app.common.enum import UserRole
from app.common.exceptions import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.user import UserDetailResponse, UserResponse
from app.service import userService

AdminRouter = APIRouter(
    tags = ["Admin: User"],
    dependencies = [
        Depends(required_role([UserRole.ADMIN]))
    ]
)
@AdminRouter.get(
    path = "/users",
    name  = "List of users",
    status_code=200,
    response_model=APIResponse[List[UserResponse]],
)
async def get_users(
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50),
    role: Optional[UserRole] = Query(default=None,description="Lọc theo vai trò người dùng"),
    name: Optional[str] = Query(default=None,description="Lọc theo tên người dùng"),
    phone: Optional[str] = Query(default=None,description="Lọc theo số điện thoại"),
    address: Optional[str] = Query(default=None,description="Lọc theo địa chỉ người dùng"),
):
    conditions = {}
    if role: 
        conditions['role'] = {
            "$regex": role,
            "$options": "i"
        }
    if name:
        conditions['name'] = {
            "$regex": name,
            "$options": "i"
        }
    if phone:
        conditions['phone'] = {
            "$regex": phone,
            "$options": "i"
        }
    if address:
        conditions['address'] = {
            "$regex": address,
            "$options": "i"
        }
    users = await userService.find_many_by(
        conditions,
        skip=(page - 1) * limit,
        limit=limit
    )
    return APIResponse(
        data=users
    )

@AdminRouter.get(
    path = "/users/{id}",
    name  = "Detail user",
    status_code=200,
    response_model=APIResponse[UserDetailResponse],
)
async def get_user(id: PydanticObjectId):
    user = await userService.find_one_by(value=id)
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
)
async def delete_user(id: PydanticObjectId, request: Request):
    user = await userService.find_one_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Người dùng {id} không tồn tại"
        )
    if str(user.id) == str(request.state.user_id):
        raise HTTP_403_FORBIDDEN(
            message = "Bạn không thể tự xóa tài khoản của mình."
        )
    await userService.delete(id)
    return APIResponse(
        data = True
    )