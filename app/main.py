from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api
from app.common.api_message import KeyResponse
from app.common.http_exception import HTTP_ERROR
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
    title = "QRBusiness Backend",
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Endpoint
app.include_router(api)
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
@app.exception_handler(HTTP_ERROR)
async def exception_handler(_: Request, exc: HTTP_ERROR):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message":KeyResponse.VALIDATION_ERROR,
            "error":[
                f"{error['msg']} {error['loc']}" for error in exc.errors()
            ]
        }
    )