import time
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from app.common.enum import APIError,APIMessage
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.time()
            return await call_next(request)
        except Exception as e:
            duration = time.time() - start_time
            logger.error({
                "host": request.client.host,
                "user-agent":request.headers.get("user-agent","unknown"),
                "method": request.method,
                "path": request.url.path,
                "duration": duration,
                "status_code": 500,
                "error": e.__class__.__name__,
            })
            return JSONResponse(
                status_code=500,
                content = {
                    "error":APIError.SERVER_ERROR,
                    "message": APIMessage.SERVER_ERROR
                }
            )