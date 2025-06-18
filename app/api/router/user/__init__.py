from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request
from app.common.exceptions import HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND
from app.api.dependency import login_required, required_role,required_permissions
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
    response_model=APIResponse,
    dependencies = [
        Depends(required_permissions(permissions=[
            "view.user"
        ]))
    ]
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
    response_model=APIResponse,
    dependencies = [
        Depends(required_permissions(permissions=[
            "create.user"
        ]))
    ]
)
async def post_user(data:Staff,request:Request):
    data = data.model_dump()
    user_scope = request.state.user_scope
    business = await businessService.find_one_by(value=user_scope)
    data['scope'] = business
    staff = await userService.create(data)
    return APIResponse(data=staff)

@apiRouter.post(
    path = "/{id}",
    name = "Mở/Khóa người dùng/nhân viên",
    response_model=APIResponse,
    dependencies = [
        Depends(required_permissions(permissions=[
            "update.user"
        ])),
    ]
)
async def lock_unlock_user(id:PydanticObjectId,request:Request):
    user = await userService.find_one_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy người dùng")
    user_request_scope = request.state.user_scope
    if user_request_scope is None or user_request_scope == str(user.business.id):
        user = await userService.update(
            id=id,
            data = {
                "available": not user.available
            }
        )
        return APIResponse(data=user)
    raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")