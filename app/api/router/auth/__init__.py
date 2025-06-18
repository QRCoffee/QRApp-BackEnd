from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required
from app.common.enum import APIError, APIMessage
from app.common.exceptions import HTTP_401_UNAUTHORZIED
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.schema.user import Auth, Token
from app.service import userService

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
    user_scope = str(user.scope.id) if user.scope else None
    user_group = str(user.group.id) if user.group else None
    user_role = user.role
    user_permissions = [permission.code for permission in user.permissions]
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
    response_model=APIResponse,
    dependencies = [
        Depends(login_required)
    ]
)
async def me(request:Request):
    user = await userService.find_one_by(value=request.state.user_id)
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
    user = await userService.find_one_by(value=request.state.user_id)
    return APIResponse(data=user.permissions)