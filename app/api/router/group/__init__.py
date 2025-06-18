from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request

from app.api.dependency import (login_required, required_permissions,
                                required_role)
from app.common.exceptions import (HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND, HTTP_409_CONFLICT)
from app.common.responses import APIResponse
from app.schema.group import GroupCreate
from app.service import businessService, groupService

apiRouter = APIRouter(
    tags = ['Group'],
    prefix="/group",
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
                'Admin',
                'BusinessOwner'
            ])
        ),
    ]
)

@apiRouter.post(
    path = "",
    name = "Tạo Group",
    response_model=APIResponse,
    dependencies = [
        Depends(required_permissions(permissions=[
                "create.group"
            ])
        ),
    ]
)
async def post_group(data:GroupCreate,request:Request):
    data = data.model_dump()
    business = await businessService.find_one_by(value=request.state.user_scope)
    data['scope'] = business
    group_in_business = await groupService.find_by_business(business.id)
    if any(group.name.lower() == data["name"].lower() for group in group_in_business):
        raise HTTP_409_CONFLICT(f"Đã có nhóm {data["name"]} tại doanh nghiệp/scope này")
    group = await groupService.create(data)
    return APIResponse(data=group)

@apiRouter.delete(
    path = "/{id}",
    name = "Xóa Group",
    response_model=APIResponse,
    dependencies = [
        Depends(required_permissions(permissions=[
                "delete.group"
            ])
        ),
    ]
)
async def delete_group(id:PydanticObjectId,request:Request):
    group = await groupService.find_one_by(value=id)
    if group is None:
        raise HTTP_404_NOT_FOUND(f"Group {id} không tồn tại")
    if request.state.user_scope == str(group.scope.id):
        if await groupService.delete(id):
            return APIResponse(data=True)
        else:
            raise HTTP_400_BAD_REQUEST("Có lỗi khi xảy ra")
    raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")