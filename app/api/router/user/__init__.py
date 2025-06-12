from fastapi import APIRouter,Depends
from app.common.responses import APIResponse
from app.api.dependency import permissions
apiRouter = APIRouter(
    tags = ["User"],
)

@apiRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse,
    response_model_exclude={"data":{"password"}}
)
async def profile(payload = Depends(permissions())):
    return APIResponse(
        data=payload
    )