from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required, required_role
from app.common.responses import APIResponse
from app.schema.user import Staff
from app.service import businessService, userService

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
    name = "Xem người dùng/nhân viên",
    response_model=APIResponse
)
async def get_users(request:Request):
    user_scope = request.state.user_scope
    if user_scope is None:
        users = await userService.find_many_by({})
    else:
        users = await userService.find_many_by({
            "scope._id": PydanticObjectId(user_scope)
        })
    return APIResponse(data=users)

@apiRouter.post(
    path = "",
    name = "Tạo người dùng/nhân viên",
    response_model=APIResponse
)
async def post_user(data:Staff,request:Request):
    data = data.model_dump()
    user_scope = request.state.user_scope
    business = await businessService.find_one_by(value=user_scope)
    data['scope'] = business
    staff = await userService.create(data)
    return APIResponse(data=staff)