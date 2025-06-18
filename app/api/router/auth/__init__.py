from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required
from app.common.enum import APIError, APIMessage
from app.common.exceptions import HTTP_401_UNAUTHORZIED
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.schema.user import Auth, Token,FullUserResponse
from app.service import permissionService, userService

apiRouter = APIRouter(
    tags = ["Auth - Self"],
)

@apiRouter.post(
    path = "/sign-in",
    name = "Đăng nhập",
    status_code=200,
    response_model=APIResponse[Token],
)
async def sign_in(data:Auth):
    user = await userService.find_one_by(by="username", value=data.username)
    if not user or not user.verify_password(data.password):
        raise HTTP_401_UNAUTHORZIED(
            error= APIError.INVALID_CREDENTIALS,
            message=APIMessage.INVALID_CREDENTIALS,
        )
    user_id = str(user.id)
    user_role = str(user.role)
    user_scope = str(user.business.to_ref().id) if user.business else None
    user_group = str(user.group.to_ref().id) if user.group else None
    user_permissions = [permission.to_ref().id for permission in user.permissions]
    for index,permission in enumerate(user_permissions):
        permission = await permissionService.find_one_by(value=permission)
        user_permissions[index] = permission.code
    payload  = {
        "user_id": user_id,
        "user_scope": user_scope,
        "user_group": user_group,
        "user_role":user_role,
        "user_permissions": user_permissions,
    }
    access_token=ACCESS_JWT.encode(payload)
    refresh_token=REFRESH_JWT.encode(payload,session=True)
    return APIResponse(
        data = Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    )

@apiRouter.get(
    path = "/me",
    name = "Xem thông tin cá nhân",
    status_code=200,
    response_model=APIResponse[FullUserResponse],
    dependencies = [
        Depends(login_required)
    ]
)
async def me(request:Request):
    user = await userService.find_one_by(value=request.state.user_id)
    await user.fetch_all_links()
    return APIResponse(data=user)
    

@apiRouter.get(
    path = "/permissions",
    name = "Xem quyền của cá nhân",
    status_code=200,
    response_model=APIResponse,
    dependencies = [
        Depends(login_required)
    ]
)
async def me(request:Request):
    permissions = []
    for permission in request.state.user_permissions:
        p = await permissionService.find_one_by(
            by = "code",
            value = permission,
        )
        permissions.append(p)
    return APIResponse(data=permissions)