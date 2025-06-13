import time

from fastapi import Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.enum import APIError, APIMessage


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            duration = time.time() - start_time
            status_code = 500
            error = APIError.SERVER_ERROR
            message = APIMessage.SERVER_ERROR
            if isinstance(e,ResponseValidationError):
                status_code = 422
                error = APIError.VALIDATION_ERROR
                message = [f"{error['msg']} {error['loc']}" for error in e.errors()]
            # Ghi log lỗi
            logger.error({
                "host": request.client.host,
                "user_agent": request.headers.get("user-agent", "unknown"),
                "method": request.method,
                "path": request.url.path,
                "duration": duration,
                "status_code": 500,
                "error": type(e).__name__,
            })
            # Trả JSON lỗi
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": error,
                    "message": message,
                }
            )