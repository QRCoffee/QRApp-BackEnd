from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required, required_role
from app.common.enum import APIError, APIMessage, UserRole
from app.common.exceptions import HTTP_401_UNAUTHORZIED
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.db import Redis as SessionManager
from app.schema.user import Auth, Manager, Session, Token, UserDetailResponse
from app.service import userService

apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
    response_model=APIResponse[UserDetailResponse],
    dependencies = [
        Depends(login_required),
        Depends(required_role([UserRole.ADMIN])
        ),
    ]
)
async def sign_up(data:Manager):
    user = await userService.create(data)
    return APIResponse(
        data=user
    )

@apiRouter.post(
    path = "/sign-in",
    name  = "Sign In",
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
    restaurant_id = None
    permissions = [permission.code for permission in user.permissions]
    if restaurant := user.restaurant:
        restaurant_id = str(restaurant.id)
    payload  = {
        "user_id":user_id,
        "restaurant_id": restaurant_id,
        "role": user.role,
        "permissions": permissions,
    }
    access_token=ACCESS_JWT.encode(payload)
    refresh_token=REFRESH_JWT.encode(payload,session=True)
    return APIResponse(
        data = Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    )

@apiRouter.post(
    path = "/sign-out",
    name  = "Sign Out",
    status_code=200,
    response_model=APIResponse,
    response_model_exclude={"data"},
    dependencies = [
        Depends(login_required),
    ]
)
async def sign_out(data:Session, request: Request):
    user_id = request.state.user_id
    if SessionManager.get(user_id) != data.refresh_token:
        raise HTTP_401_UNAUTHORZIED(
            error= APIError.SESSION_INVALID,
            message="đăng xuất thất bại"
        )
    SessionManager.delete(user_id)
    return APIResponse()