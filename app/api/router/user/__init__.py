from fastapi import APIRouter,Depends
from app.common.responses import APIResponse
from app.schema.user import UserResponse
from app.api.dependency import permissions
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