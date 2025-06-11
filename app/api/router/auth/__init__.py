from fastapi import APIRouter, Depends

from app.api.dependency import login_required
from app.common.exceptions import ConflictException, UnauthorizedException
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.db import Redis
from app.models import User
from app.schema.user import SignIn, SignOut, SignUp
from app.service.base import Service

apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
    response_model=APIResponse[User],
    response_model_exclude={
        "data": {
            "password",
        }
    },
    # dependencies=[
    #     Depends(login_required)
    # ],
)
async def sign_up(data:SignUp):
    user_service = Service[User, SignUp, SignUp](User)
    if await user_service.find_by(by="username", value=data.username):
        raise ConflictException("username has been used")
    user = await user_service.create(data)
    return APIResponse(
        message="register successfully",
        data=user,
    )

@apiRouter.post(
    path = "/sign-in",
    name  = "Sign In",
    status_code=201,
    response_model=APIResponse[User],
    response_model_exclude={
        "data": {
            "password",
        }
    },
    dependencies=[
        Depends(login_required)
    ],
)
async def sign_up(data:SignIn):
    user_service = Service[User, SignUp, SignUp](User)
    if await user_service.find_by(by="username", value=data.username):
        raise ConflictException("username has been used")
    user = await user_service.create(data)
    return APIResponse(
        message="register successfully",
        data=user,
    )

