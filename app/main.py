from contextlib import asynccontextmanager
from fastapi import FastAPI, Request,WebSocket,WebSocketDisconnect,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from app.service import userService
from app.api.router import apiRouter
from app.common.exceptions import APIException
from app.core.middleware import ExceptionMiddleware, LoggingMiddleware
from app.db import Mongo
from app.common.enum import UserRole
from app.common.enum import APIError
from app.socket import manager
from app.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):    
    # on_startup
    await Mongo.initialize()
    if not await userService.find_by(
        "username",
        "admin"
    ):
        await userService.create({
            "username":settings.ADMIN_USERNAME,
            "password":settings.ADMIN_PASSWORD,
            "role":UserRole.ADMIN,
        })
    logger.info("Application startup complete.")
    yield
    # on_shutdown
    logger.info("Waiting for application shutdown.")

app = FastAPI(
    title = "QRApp Backend",
    debug = False,
    lifespan = lifespan,
    version = settings.APP_VERSION,
)
# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionMiddleware)
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