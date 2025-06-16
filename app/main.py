from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.router import apiRouter
from app.common.enum import APIError, PermissionCode, UserRole
from app.common.exceptions import APIException
from app.core.config import settings
from app.core.middleware import LoggingMiddleware
from app.db import Mongo
from app.schema.permission import PermissionCreate
from app.schema.user import Administrator
from app.service import permissionService, userService
from app.socket import manager


@asynccontextmanager
async def lifespan(_: FastAPI):    
    # on_startup
    await Mongo.initialize()
    for permission in PermissionCode:
        if await permissionService.find_one_by(
            by="code",
            value=permission.code
        ) is None:
            await permissionService.create(PermissionCreate(
                code = permission.code,
                description = permission.description,
            ))
    if not await userService.find_one_by(
        by = "username",
        value = "admin"
    ):
        await userService.create(Administrator(
            username = settings.ADMIN_USERNAME,
            password = settings.ADMIN_PASSWORD,
            permissions = PermissionCode.get_permissions_by_role(UserRole.ADMIN)
        ))        
    yield
    # on_shutdown
app = FastAPI(
    title = "QRApp Backend",
    description="""
    * 📚 Swagger UI: `/docs`
    * 📖 ReDoc: `/redoc`
    """,
    debug = False,
    lifespan = lifespan,
    version = settings.APP_VERSION,
)
# Middleware
app.add_middleware(LoggingMiddleware)
# Endpoint
app.include_router(apiRouter)
# WebSocket
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
# Handle Exception
@app.exception_handler(APIException)
async def exception_handler(_: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message":APIError.VALIDATION_ERROR,
            "error":[
                f"{error['msg']} {error['loc']}" for error in exc.errors()
            ]
        }
    )