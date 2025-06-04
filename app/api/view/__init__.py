from fastapi import APIRouter, Request
from api.view.response import HTTP_404_NOT_FOUND
from .auth import apiRouter as authRouter

apiRouter = APIRouter()
# Handle Undefined API
apiRouter.include_router(authRouter)
@apiRouter.api_route(
    path = "/{path:path}",
    methods = ["GET", "POST", "DELETE","PUT","PATCH","OPTIONS"],
    include_in_schema=False,
)
async def catch_all(path: str, request: Request):
    return HTTP_404_NOT_FOUND(
        error = f"{request.method} {request.url.path} is undefined"
    )