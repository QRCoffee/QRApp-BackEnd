import time

from fastapi import Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
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
            # Xác định loại lỗi & mã phản hồi
            error_mapping = {
                ValidationError: {
                    "status_code": 422,
                    "error": APIError.VALIDATION_ERROR.value,
                    "message": [f"{error['msg']} {error['loc']}" for error in e.errors()]
                },
                ResponseValidationError: {
                    "status_code": 422, 
                    "error": APIError.VALIDATION_ERROR.value,
                    "message": [f"{error['msg']} {error['loc']}" for error in e.errors()]
                },
                AttributeError: {
                    "status_code": 400,
                    "error": APIError.BAD_REQUEST.value,
                    "message": str(e)
                }
            }
            # Get error config or use default
            error_config = error_mapping.get(type(e), {
                "status_code": 500,
                "error": APIError.SERVER_ERROR,
                "message": APIMessage.SERVER_ERROR
            })
            # Ghi log lỗi
            logger.error({
                "host": request.client.host,
                "user_agent": request.headers.get("user-agent", "unknown"),
                "method": request.method,
                "path": request.url.path,
                "duration": duration,
                "status_code": error_config.get("status_code"),
                "error": type(e).__name__,
            })
            # Trả JSON lỗi
            return JSONResponse(
                status_code=error_config.get("status_code"),
                content={
                    "error": error_config.get("error"),
                    "message": error_config.get("message")
                }
            )