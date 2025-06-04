from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from api.view.response import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_422_VALIDATION_ERROR
from pydantic import ValidationError
class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e,ValidationError):
                return HTTP_422_VALIDATION_ERROR(
                    error = e.errors(),
                )
            return HTTP_500_INTERNAL_SERVER_ERROR(
                error = e
            )