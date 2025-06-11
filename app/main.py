from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from app.api.router import apiRouter
from app.common.exceptions import APIException
from app.core.middleware import ExceptionMiddleware, LoggingMiddleware
from app.db import Mongo


@asynccontextmanager
async def lifespan(_: FastAPI):    
    # on_startup
    await Mongo.initialize()
    logger.info("Application startup complete.")
    yield
    # on_shutdown
    logger.info("Waiting for application shutdown.")

app = FastAPI(
    title = "QRApp Backend",
    debug = False,
    lifespan = lifespan,
)
# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionMiddleware)
# Endpoint
app.include_router(apiRouter)
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
        status_code=422,
        content={
            "message":"Validation Error",
            "error":exc.errors()
        }
    )