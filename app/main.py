from contextlib import asynccontextmanager
from api.view import apiRouter
from core import settings
from db import mysql
from fastapi.responses import JSONResponse
from db.model import User
from fastapi import FastAPI
from api.middleware import ExceptionMiddleware, LoggingMiddleware
from fastapi.exceptions import RequestValidationError
from api.view.response import HTTP_422_VALIDATION_ERROR
from api.view.response import CustomHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):    
    # on_startup
    mysql.init_db(
        tables=[
            User.__table__,
        ]
    )
    yield
    # on_shutdown
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.include_router(apiRouter)
# Middleware
app.add_middleware(LoggingMiddleware)
# Handle Exception
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return HTTP_422_VALIDATION_ERROR(error=exc.errors())
app.add_middleware(ExceptionMiddleware)