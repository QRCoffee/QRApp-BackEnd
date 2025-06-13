from fastapi import APIRouter, Depends

from app.api.dependency import permissions
from app.common.enum import APIError, APIMessage, UserRole
from app.common.exceptions import HTTP_401_UNAUTHORZIED
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.db import Redis as SessionManager
from app.schema.user import (Administrator, Auth, Manager, Session, Token,
                             UserResponse)
from app.service import userService

apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
    response_model=APIResponse[UserResponse],
)
async def sign_up(data:Manager | Administrator, _ = Depends(permissions([UserRole.ADMIN]))):
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
    user = await userService.find_by(by="username", value=data.username)
    if not user or not user.verify_password(data.password):
        raise HTTP_401_UNAUTHORZIED(
            error= APIError.INVALID_CREDENTIALS,
            message=APIMessage.INVALID_CREDENTIALS,
        )
    return APIResponse(
        data = Token(
            access_token=ACCESS_JWT.encode(user),
            refresh_token=REFRESH_JWT.encode(user,session=True)
        )
    )

@apiRouter.post(
    path = "/sign-out",
    name  = "Sign Out",
    status_code=200,
    response_model=APIResponse,
    response_model_exclude={"data"}
)
async def sign_out(data:Session, payload = Depends(permissions())):
    user_id = payload.get("_id")
    if SessionManager.get(user_id) != data.refresh_token:
        raise HTTP_401_UNAUTHORZIED(
            error= APIError.SESSION_INVALID,
            message="đăng xuất thất bại"
        )
    SessionManager.delete(user_id)
    return APIResponse()