from fastapi import APIRouter,Depends
from app.common.responses import APIResponse
from app.api.dependency import permissions
from app.schema.user import UserResponse

ManageRouter = APIRouter(
    tags = ["User: Manage"],
)
@ManageRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse[UserResponse],
)
async def profile(payload = Depends(permissions())):
    return APIResponse(
        data=payload
    )

@ManageRouter.get(
    path = "/restaurant",
    name  = "My Restaurant",
    status_code=200,
    response_model=APIResponse,
)
async def profile(payload = Depends(permissions())):
    return APIResponse(
        data=payload.get("restaurant")
    )