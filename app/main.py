from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import apiRouter
from app.common.enum import APIError
from app.common.exceptions import APIException
from app.core.config import settings
from app.core.middleware import LoggingMiddleware
from app.db import Mongo
from app.socket import manager


@asynccontextmanager
async def lifespan(_: FastAPI):    
    # on_startup
    await Mongo.initialize()
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn (origin)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Cho phép tất cả header
)
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