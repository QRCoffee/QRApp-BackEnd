from fastapi import APIRouter, Depends

from app.api.dependency import login_required
from app.common.exceptions import ConflictException, UnauthorizedException
from app.common.responses import APIResponse
from app.core.security import ACCESS_JWT, REFRESH_JWT
from app.db import Redis
from app.models import User
from app.schema.auth import SignIn,SignUp,Session,SignOut
from app.service import userService

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
    dependencies=[
        Depends(login_required)
    ],
)
async def sign_up(data:SignUp,payload = Depends(login_required)):
    if payload.get("role") != "Manager":
        raise UnauthorizedException("không đủ quyền")
    if await userService.find_by(by="username", value=data.username):
        raise ConflictException("username đã tồn tại")
    user = await userService.create(data)
    return APIResponse(
        message="đăng kí thành công",
        data=user,
    )

@apiRouter.post(
    path = "/sign-in",
    name  = "Sign In",
    status_code=200,
    response_model=APIResponse[Session],
)
async def sign_in(data:SignIn):
    user = await userService.find_by(by="username", value=data.username)
    if not user or not user.verify_password(data.password):
        raise UnauthorizedException("sai thông tin đăng nhập")
    return APIResponse(
        message = "đăng nhập thành công",
        data = Session(
            access_token=ACCESS_JWT.encode(user),
            refresh_token=REFRESH_JWT.encode(user,session=True)
        )
    )

@apiRouter.post(
    path = "/sign-out",
    name  = "Sign Out",
    status_code=200,
)
async def sign_in(data:SignOut, payload = Depends(login_required)):
    user_id = payload.get("_id")
    if Redis.get(user_id) != data.refresh_token:
        raise UnauthorizedException(
            message="đăng xuất thất bại"
        )
    Redis.delete(user_id)
    return APIResponse(
        message="đăng xuất thành công",
        data = None,
    )    