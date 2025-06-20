from fastapi import APIRouter, Request

from app.api.router.area import apiRouter as areaRouter
from app.api.router.auth import apiRouter as authRouter
from app.api.router.branch import apiRouter as branchRouter
from app.api.router.business import apiRouter as businessRouter
from app.api.router.business_type import apiRouter as businesstypeRouter
from app.api.router.group import apiRouter as groupRouter
from app.api.router.user import apiRouter as userRouter
from app.common.http_exception import HTTP_404_NOT_FOUND

api = APIRouter()
api.include_router(authRouter)
api.include_router(businesstypeRouter)
api.include_router(businessRouter)
api.include_router(branchRouter)
api.include_router(groupRouter)
api.include_router(userRouter)
api.include_router(areaRouter)
# Handle Undefined API
@api.api_route(
    path = "/{path:path}",
    methods = ["GET", "POST", "DELETE","PUT","PATCH","OPTIONS"],
    include_in_schema=False,
)
async def catch_all(path: str, request: Request):
    raise HTTP_404_NOT_FOUND(
        error="NOT FOUND",
        message=f"{request.method} {request.url.path} is undefined"
    )