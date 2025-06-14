from fastapi import APIRouter, Request

from app.api.router.auth import apiRouter as authRouter
from app.api.router.restaurant import apiRouter as restaurantRouter
from app.api.router.user import apiRouter as userRouter
from app.common.enum import APIError
from app.common.exceptions import HTTP_404_NOT_FOUND

apiRouter = APIRouter()
apiRouter.include_router(authRouter)
apiRouter.include_router(userRouter)
apiRouter.include_router(restaurantRouter)
# Handle Undefined API
@apiRouter.api_route(
    path = "/{path:path}",
    methods = ["GET", "POST", "DELETE","PUT","PATCH","OPTIONS"],
    include_in_schema=False,
)
async def catch_all(path: str, request: Request):
    raise HTTP_404_NOT_FOUND(
        error=APIError.NOT_FOUND,
        message=f"{request.method} {request.url.path} is undefined"
    )