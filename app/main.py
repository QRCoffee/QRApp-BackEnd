import logging
from app.db import MySQL
from app.models import User
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.router import apiRouter
from app.core.middleware import LoggingMiddleware,ExceptionMiddleware
from contextlib import asynccontextmanager
from app.common.exceptions import APIException
from fastapi.exceptions import RequestValidationError

@asynccontextmanager
async def lifespan(_: FastAPI):    
    # on_startup
    MySQL.initiate(
        tables=[
            User.__table__,
        ]
    )
    logging.getLogger(settings.LOG_NAME).info("Application startup complete.")
    yield
    # on_shutdown
    logging.getLogger(settings.LOG_NAME).info("Waiting for application shutdown.")

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