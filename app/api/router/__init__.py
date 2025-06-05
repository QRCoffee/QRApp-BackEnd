from fastapi import Request
from fastapi import APIRouter
from app.common.exceptions import NotFoundException
from app.api.router.auth import apiRouter as authRouter
apiRouter = APIRouter()
apiRouter.include_router(authRouter)
# Handle Undefined API
@apiRouter.api_route(
    path = "/{path:path}",
    methods = ["GET", "POST", "DELETE","PUT","PATCH","OPTIONS"],
    include_in_schema=False,
)
async def catch_all(path: str, request: Request):
    raise NotFoundException(f"{request.method} {request.url.path} is undefined")