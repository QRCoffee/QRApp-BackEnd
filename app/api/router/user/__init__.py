from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request,BackgroundTasks
from typing import List
from app.api.dependency import (login_required, required_permissions,
                                required_role)
from app.common.api_message import KeyResponse, get_message
from app.common.api_response import Response
from app.common.http_exception import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.schema.user import Staff,UserResponse,FullUserResponse
from app.service import businessService, userService
from app.db import Redis

apiRouter = APIRouter(
    tags = ["User"],
    prefix = "/users",
    dependencies = [
        Depends(login_required),
        Depends(required_role(
            role=[
                'Admin',
                'BusinessOwner'
            ])
        ),
    ]
)

@apiRouter.get(
    path = "",
    name = "Xem danh sách",
    response_model=Response[List[UserResponse]],
    dependencies = [
        Depends(required_permissions(permissions=[
            "view.user"
        ]))
    ]
)
async def get_users(request:Request):
    user_scope = request.state.user_scope
    if user_scope is None:
        users = await userService.find_many({})
    else:
        users = await userService.find_many({
            "business.$id": PydanticObjectId(user_scope),
            "role": "Staff"
        })
    return Response(data=users)

@apiRouter.get(
    path = "/{id}",
    name = "Xem chi tiết",
    response_model=Response[FullUserResponse],
    dependencies = [
        Depends(required_permissions(permissions=[
            "view.user"
        ]))
    ]
)
async def get_user(id:PydanticObjectId,request:Request):
    staff = await userService.find(id)
    if staff is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy")
    user_scope = request.state.user_scope
    staff_scope = str(staff.business.to_ref().id)
    if user_scope is not None and user_scope != staff_scope:
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    await staff.fetch_all_links()
    return Response(data=staff)

@apiRouter.post(
    path = "",
    name = "Tạo người dùng/nhân viên",
    response_model=Response[UserResponse],
    dependencies = [
        Depends(required_permissions(permissions=[
            "create.user"
        ]))
    ]
)
async def post_user(data:Staff,request:Request):
    data = data.model_dump()
    user_scope = request.state.user_scope
    business = await businessService.find(user_scope)
    data['business'] = business
    staff = await userService.insert(data)
    return Response(data=staff)

@apiRouter.post(
    path = "/{id}",
    name = "Mở/Khóa người dùng/nhân viên",
    response_model=Response[UserResponse],
    dependencies = [
        Depends(required_permissions(permissions=[
            "update.user"
        ])),
    ]
)
async def lock_unlock_user(id:PydanticObjectId,request:Request,task: BackgroundTasks):
    def remove_session(user_id: str):
        Redis.delete(user_id)
    user = await userService.find(id)
    if user is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy")
    user_request_scope = request.state.user_scope
    if user_request_scope is None or user_request_scope == str(user.business.id):
        user = await userService.update(
            id=id,
            data = {
                "available": not user.available
            }
        )
        task.add_task(remove_session,str(id))
        return Response(data=user)
    raise HTTP_403_FORBIDDEN(get_message(KeyResponse.PERMISSION_DENIED))