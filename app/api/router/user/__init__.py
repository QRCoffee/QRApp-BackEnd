from fastapi import APIRouter,Depends
from typing import List
from app.common.responses import APIResponse
from app.common.exceptions import HTTP_404_NOT_FOUND
from app.common.enum import UserRole,APIError,APIMessage
from beanie import PydanticObjectId
from app.schema.user import UserResponse
from app.api.dependency import permissions
from app.service import userService
apiRouter = APIRouter(
    tags = ["User"],
)

@apiRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse[UserResponse],
)
async def profile(payload = Depends(permissions())):
    return APIResponse(
        data=payload
    )

@apiRouter.get(
    path = "/users",
    name  = "List of users",
    status_code=200,
    response_model=APIResponse[List[UserResponse]],
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ]
)
async def get_users():
    users = await userService.find_all()
    return APIResponse(
        data=users
    )

@apiRouter.get(
    path = "/users/{id}",
    name  = "Detail user",
    status_code=200,
    response_model=APIResponse[UserResponse],
    dependencies=[
        Depends(permissions([UserRole.ADMIN]))
    ]
)
async def get_users(id: PydanticObjectId):
    user = await userService.find_by(value=id)
    if user is None:
        raise HTTP_404_NOT_FOUND(
            message = f"Người dùng {id} không tồn tại"
        )
    return APIResponse(
        data=user
    )