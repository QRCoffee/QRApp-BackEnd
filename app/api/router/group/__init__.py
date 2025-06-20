from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request

from app.api.dependency import (login_required, required_permissions,
                                required_role)
from app.common.api_message import KeyResponse, get_message
from app.common.api_response import Response
from app.common.http_exception import (HTTP_400_BAD_REQUEST,
                                       HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                       HTTP_409_CONFLICT)
from app.schema.group import GroupCreate, GroupResponse
from app.service import (businessService, groupService, permissionService,
                         userService)

apiRouter = APIRouter(
    tags = ['Group'],
    prefix="/groups",
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
                'Admin',
                'BusinessOwner'
            ])
        ),
    ]
)

@apiRouter.get(
    path = "",
    name = "Xem danh sách nhóm (Thuộc quyền sở hữu)",
    response_model=Response[List[GroupResponse]],
)
async def get_groups(request:Request):
    groups = await groupService.find_many(
        {
            "business._id":PydanticObjectId(request.state.user_scope)
        },
        fetch_links=True
    )
    return Response(data=groups)

@apiRouter.get(
    path = "/{id}",
    name = "Xem nhóm (Thuộc quyền sở hữu)",
    response_model=Response[GroupResponse],
)
async def get_group(id:PydanticObjectId,request:Request):
    group = await groupService.find(id)
    if PydanticObjectId(request.state.user_scope) == group.business.to_ref().id:
        await group.fetch_link("permissions")
        return Response(data=group)
    raise HTTP_403_FORBIDDEN(get_message(KeyResponse.PERMISSION_DENIED))

@apiRouter.post(
    path = "",
    name = "Tạo nhóm",
    response_model=Response[GroupResponse],
    dependencies = [
        Depends(required_permissions(permissions=[
                "create.group"
            ])
        ),
    ]
)
async def post_group(data:GroupCreate,request:Request):
    data = data.model_dump()
    business = await businessService.find(request.state.user_scope)
    data['business'] = business
    group_in_business = await groupService.find_many({
        "business.$id":PydanticObjectId(request.state.user_scope)
    })
    if any(group.name.lower() == data["name"].lower() for group in group_in_business):
        raise HTTP_409_CONFLICT(f"Đã có nhóm {data["name"]} tại doanh nghiệp/scope này")
    group = await groupService.insert(data)
    return Response(data=group)


@apiRouter.delete(
    path = "/{id}",
    name = "Xóa nhóm",
    status_code=204,
    dependencies = [
        Depends(required_permissions(permissions=[
                "delete.group"
            ])
        ),
    ]
)
async def delete_group(id:PydanticObjectId,request:Request):
    group = await groupService.find(id)
    if group is None:
        raise HTTP_404_NOT_FOUND(f"Không tìm thấy")
    if PydanticObjectId(request.state.user_scope) == group.business.to_ref().id:
        if await groupService.delete(id):
            return True
        else:
            raise HTTP_400_BAD_REQUEST("Có lỗi khi xảy ra")
    raise HTTP_403_FORBIDDEN(get_message(KeyResponse.PERMISSION_DENIED))

@apiRouter.post(
    path = "/{id}/permissions",
    name = "Cấp quyền",
    response_model=Response[GroupResponse]
)
async def give_permissions(id:PydanticObjectId,data: List[str | PydanticObjectId], request:Request):
    # Check scope
    group = await groupService.find(id)
    if group is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy")
    user = await userService.find(request.state.user_id)
    if user.business.to_ref().id != group.business.to_ref().id:
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    # Grant permission
    grant_permissions = await permissionService.find_many(
        conditions={
            "$or": [
                {"_id": {"$in": [v for v in data if isinstance(v, PydanticObjectId)]}},
                {"code": {"$in": [v for v in data if isinstance(v, str)]}},
            ]
        }
    )
    if not grant_permissions:
        return Response(data=group)
    grant_permission_ids = [p.id for p in grant_permissions]
    # User permission
    user_permissions = [permission.to_ref().id for permission in user.permissions]
    # Check
    if any(permission not in user_permissions for permission in grant_permission_ids):
        raise HTTP_403_FORBIDDEN("Cần có quyền để cấp")
    group = await groupService.update_one(
        id = id,
        conditions={
            "$addToSet": {
                "permissions": {
                    "$each": [p.to_ref() for p in grant_permissions]
                }
            }
        }
    )
    await group.fetch_link("permissions")
    return Response(data=group)

@apiRouter.delete(
    path = "/{id}/permissions",
    name = "Thu hồi quyền",
    response_model=Response[GroupResponse],
)
async def delete_permissions(id:PydanticObjectId,data: List[str | PydanticObjectId], request:Request):
    # Check scope
    group = await groupService.find(id)
    if group is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy")
    user = await userService.find(request.state.user_id)
    if user.business.to_ref().id != group.business.to_ref().id:
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    # Grant permission
    grant_permissions = await permissionService.find_many(
        conditions={
            "$or": [
                {"_id": {"$in": [v for v in data if isinstance(v, PydanticObjectId)]}},
                {"code": {"$in": [v for v in data if isinstance(v, str)]}},
            ]
        }
    )
    if not grant_permissions:
        return Response(data=group)
    group = await groupService.update_one(
        id=id,
        conditions={
            "$pull": {
                "permissions": {
                    "$in": [p.to_ref() for p in grant_permissions]
                }
            }
        }
    )
    await group.fetch_link("permissions")
    return Response(data=group)